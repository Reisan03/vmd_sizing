# -*- coding: utf-8 -*-
#
import os
import re
import sys
import wx
import winsound

from form.panel.FilePanel import FilePanel
from form.panel.MorphPanel import MorphPanel
from form.worker.SizingWorkerThread import SizingWorkerThread
from form.worker.LoadWorkerThread import LoadWorkerThread
from module.MMath import MRect, MVector3D, MVector4D, MQuaternion, MMatrix4x4 # noqa
from utils import MFormUtils, MFileUtils # noqa
from utils.MLogger import MLogger # noqa

logger = MLogger(__name__)


# イベント
(SizingThreadEvent, EVT_SIZING_THREAD) = wx.lib.newevent.NewEvent()
(LoadThreadEvent, EVT_LOAD_THREAD) = wx.lib.newevent.NewEvent()


class MainFrame(wx.Frame):

    def __init__(self, parent, mydir_path: str, version_name: str, logging_level: int, is_out_log: bool):
        self.version_name = version_name
        self.logging_level = logging_level
        self.is_out_log = is_out_log
        self.mydir_path = mydir_path
        
        self.worker = None
        self.load_worker = None

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"VMDサイジング ローカル版 {0}".format(self.version_name), \
                          pos=wx.DefaultPosition, size=wx.Size(600, 650), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # ファイル履歴読み込み
        self.file_hitories = MFileUtils.read_history(self.mydir_path)

        # ---------------------------------------------

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.note_ctrl = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        # self.note_ctrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        self.note_ctrl.SetBackgroundColour("BLUE")

        # ---------------------------------------------

        # ファイルタブ
        self.file_panel_ctrl = FilePanel(self, self.note_ctrl, 0, self.file_hitories)
        self.note_ctrl.AddPage(self.file_panel_ctrl, u"ファイル", True)

        # モーフタブ
        self.morph_panel_ctrl = MorphPanel(self, self.note_ctrl, 1)
        self.note_ctrl.AddPage(self.morph_panel_ctrl, u"モーフ", False)

        # ---------------------------------------------

        # タブ押下時の処理
        self.note_ctrl.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_change)

        # 待機中の処理
        self.Bind(wx.EVT_IDLE, self.on_idle)

        # ---------------------------------------------

        bSizer1.Add(self.note_ctrl, 1, wx.EXPAND, 5)

        # デフォルトの出力先はファイルタブのコンソール
        sys.stdout = self.file_panel_ctrl.console_ctrl

        # イベントバインド
        self.Bind(EVT_SIZING_THREAD, self.on_exec_result)
        self.Bind(EVT_LOAD_THREAD, self.on_load_result)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
    
    def on_idle(self, event: wx.Event):
        if self.worker or self.load_worker:
            self.file_panel_ctrl.gauge_ctrl.Pulse()

    def on_tab_change(self, event: wx.Event):
        if self.file_panel_ctrl.is_fix_tab:
            self.note_ctrl.ChangeSelection(self.file_panel_ctrl.tab_idx)
            event.Skip()
            return

        elif self.morph_panel_ctrl.is_fix_tab:
            self.note_ctrl.ChangeSelection(self.morph_panel_ctrl.tab_idx)
            event.Skip()
            return
    
    def set_output_vmd_path(self):
        self.file_panel_ctrl.file_set.set_output_vmd_path()

    # スレッド実行結果
    def on_exec_result(self, event: wx.Event):
        logger.info("処理時間: %s分", event.elapsed_time / 60, decoration=MLogger.DECORATION_SIMPLE)

        # 終了音を鳴らす
        if os.name == "nt":
            # Windows
            try:
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
            except Exception:
                pass

        if not event.result or self.is_out_log:
            # 何か失敗している場合かログ明示出力の場合、ログファイル出力

            # ログパス生成
            output_vmd_path = self.file_panel_ctrl.file_set.output_vmd_file_ctrl.file_ctrl.GetPath()
            output_log_path = re.sub(r'\.vmd$', '.log', output_vmd_path)

            with open(output_log_path, mode='w') as f:
                f.write(self.file_panel_ctrl.console_ctrl.GetValue())

        # ワーカー終了
        self.worker = None
        # タブ移動可
        self.release_tab()
        # フォーム有効化
        self.enable()
        # プログレス非表示
        self.file_panel_ctrl.gauge_ctrl.SetValue(0)

    # タブ移動可
    def release_tab(self):
        self.file_panel_ctrl.release_tab()
        self.morph_panel_ctrl.release_tab()

    # フォーム入力可
    def enable(self):
        self.file_panel_ctrl.enable()
        # self.morph_panel_ctrl.enable()
    
    # ファイルセットの入力可否チェック
    def is_valid(self):
        result = True
        result = self.file_panel_ctrl.file_set.is_valid(1) and result
        return result
    
    # 入力後の入力可否チェック
    def is_loaded_valid(self):
        result = True
        result = self.file_panel_ctrl.file_set.is_loaded_valid(1) and result
        return result
        
    # 読み込み
    def load(self, is_exec=False):
        result = True
        result = self.is_valid() and result

        if not result:
            # タブ移動可
            self.release_tab()
            # フォーム有効化
            self.enable()

            return result

        # 読み込み開始
        if self.load_worker:
            logger.error("まだ処理が実行中です。終了してから再度実行してください。", decoration=MLogger.DECORATION_BOX)
        else:
            # 別スレッドで実行
            self.load_worker = LoadWorkerThread(self, self.file_panel_ctrl.file_set, LoadThreadEvent, is_exec)
            self.load_worker.start()
            self.load_worker.stop_event.set()

        return result

    # 読み込み完了処理
    def on_load_result(self, event: wx.Event):
        # タブ移動可
        self.release_tab()
        # フォーム有効化
        self.enable()
        # ワーカー終了
        self.load_worker = None
        # プログレス非表示
        self.file_panel_ctrl.gauge_ctrl.SetValue(0)

        if not event.result:
            logger.error("ファイル読み込み処理に失敗したため、処理を中断します。", decoration=MLogger.DECORATION_BOX)
            
            event.Skip()
            return False

        result = self.is_loaded_valid()

        if not result:
            # タブ移動可
            self.release_tab()
            # フォーム有効化
            self.enable()

            event.Skip()
            return False
        
        logger.info("ファイルデータ読み込みが完了しました", decoration=MLogger.DECORATION_BOX, title="OK")

        if event.is_exec:
            # そのまま実行する場合、サイジング実行処理に遷移

            # 念のため出力ファイルパス自動生成（空の場合設定）
            self.file_panel_ctrl.file_set.set_output_vmd_path()

            # フォーム無効化
            self.file_panel_ctrl.disable()
            # タブ固定
            self.file_panel_ctrl.fix_tab()

            # 履歴保持
            self.file_panel_ctrl.file_set.save()
            MFileUtils.save_history(self.mydir_path, self.file_hitories)

            if self.worker:
                logger.error("まだ処理が実行中です。終了してから再度実行してください。", decoration=MLogger.DECORATION_BOX)
            else:
                # 別スレッドで実行
                self.worker = SizingWorkerThread(self, SizingThreadEvent)
                self.worker.start()
                self.worker.stop_event.set()

            event.Skip()
            return True
        
        event.Skip()