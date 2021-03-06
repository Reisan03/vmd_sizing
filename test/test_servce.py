# -*- coding: utf-8 -*-
#
import _pickle as cPickle
import itertools
import unittest
import sys
import pathlib
import random
# このソースのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append(str(current_dir) + '/../')
sys.path.append(str(current_dir) + '/../src/')

from mmd.PmxReader import PmxReader # noqa
from mmd.VmdReader import VmdReader # noqa
from mmd.VmdWriter import VmdWriter # noqa
from mmd.PmxData import PmxModel, Vertex, Material, Bone, Morph, DisplaySlot, RigidBody, Joint # noqa
from mmd.VmdData import VmdMotion, VmdBoneFrame, VmdCameraFrame, VmdInfoIk, VmdLightFrame, VmdMorphFrame, VmdShadowFrame, VmdShowIkFrame # noqa
from module.MMath import MRect, MVector2D, MVector3D, MVector4D, MQuaternion, MMatrix4x4 # noqa
from module.MOptions import MOptions, MOptionsDataSet # noqa
from module.MParams import BoneLinks # noqa
from service.parts.StanceService import StanceService # noqa
from service.parts.MorphService import MorphService # noqa
from utils import MBezierUtils, MServiceUtils # noqa
from utils.MException import SizingException # noqa
from utils.MLogger import MLogger # noqa

logger = MLogger(__name__, level=1)


class MorphServiceTest(unittest.TestCase):

    def test_replace_morph_01(self):
        motion = VmdMotion()
        motion.morphs = {"A": {}}
        for fno, ratio in [(0, 10), (1, 20), (3, 30), (7, 0), (10, 3)]:
            motion.morphs["A"][fno] = VmdMorphFrame(fno)
            motion.morphs["A"][fno].ratio = ratio

        morph_list = []

        data_set = MOptionsDataSet(motion, None, None, None, False, False, morph_list, None, None)

        service = MorphService(None)
        service.replace_morph(0, data_set)

        self.assertEqual(["A"], sorted(list(motion.morphs.keys())))

        self.assertTrue("A" in motion.morphs)
        self.assertEqual([0, 1, 3, 7, 10], sorted(list(motion.morphs["A"].keys())))

    def test_replace_morph_02(self):
        motion = VmdMotion()
        motion.morphs = {"A": {}}
        for fno, ratio in [(0, 10), (1, 20), (3, 30), (7, 0), (10, 3)]:
            motion.morphs["A"][fno] = VmdMorphFrame(fno)
            motion.morphs["A"][fno].ratio = ratio

        morph_list = [("A", "B", 0.5)]

        data_set = MOptionsDataSet(motion, None, None, None, False, False, morph_list, None, None)

        service = MorphService(None)
        service.replace_morph(0, data_set)

        self.assertEqual(["B"], sorted(list(motion.morphs.keys())))

        self.assertTrue("B" in motion.morphs)
        self.assertEqual([0, 1, 3, 7, 10], sorted(list(motion.morphs["B"].keys())))
        self.assertEqual(5, motion.morphs["B"][0].ratio)
        self.assertEqual(10, motion.morphs["B"][1].ratio)
        self.assertEqual(15, motion.morphs["B"][3].ratio)
        self.assertEqual(0, motion.morphs["B"][7].ratio)
        self.assertEqual(1.5, motion.morphs["B"][10].ratio)

    def test_replace_morph_03(self):
        motion = VmdMotion()
        motion.morphs = {"A": {}}
        for fno, ratio in [(0, 10), (1, 20), (3, 30), (7, 0), (10, 3)]:
            motion.morphs["A"][fno] = VmdMorphFrame(fno)
            motion.morphs["A"][fno].ratio = ratio

        morph_list = [("A", "B", 0.5), ("A", "C", 2)]

        data_set = MOptionsDataSet(motion, None, None, None, False, False, morph_list, None, None)

        service = MorphService(None)
        service.replace_morph(0, data_set)

        self.assertEqual(["B", "C"], sorted(list(motion.morphs.keys())))

        self.assertTrue("B" in motion.morphs)
        self.assertEqual([0, 1, 3, 7, 10], sorted(list(motion.morphs["B"].keys())))
        self.assertEqual(5, motion.morphs["B"][0].ratio)
        self.assertEqual(10, motion.morphs["B"][1].ratio)
        self.assertEqual(15, motion.morphs["B"][3].ratio)
        self.assertEqual(0, motion.morphs["B"][7].ratio)
        self.assertEqual(1.5, motion.morphs["B"][10].ratio)

        self.assertTrue("C" in motion.morphs)
        self.assertEqual([0, 1, 3, 7, 10], sorted(list(motion.morphs["C"].keys())))
        self.assertEqual(20, motion.morphs["C"][0].ratio)
        self.assertEqual(40, motion.morphs["C"][1].ratio)
        self.assertEqual(60, motion.morphs["C"][3].ratio)
        self.assertEqual(0, motion.morphs["C"][7].ratio)
        self.assertEqual(6, motion.morphs["C"][10].ratio)

    def test_replace_morph_04(self):
        motion = VmdMotion()
        motion.morphs["A"] = {}
        for fno, ratio in [(0, 10), (1, 20), (3, 30), (7, 0), (10, 3)]:
            motion.morphs["A"][fno] = VmdMorphFrame(fno)
            motion.morphs["A"][fno].ratio = ratio

        motion.morphs["B"] = {}
        for fno, ratio in [(1, 3), (2, 5), (7, 4), (11, 2)]:
            motion.morphs["B"][fno] = VmdMorphFrame(fno)
            motion.morphs["B"][fno].ratio = ratio

        morph_list = [("A", "B", 2)]

        data_set = MOptionsDataSet(motion, None, None, None, False, False, morph_list, None, None)

        service = MorphService(None)
        service.replace_morph(0, data_set)

        self.assertEqual(["B"], sorted(list(motion.morphs.keys())))

        self.assertTrue("B" in motion.morphs)
        self.assertEqual([0, 1, 2, 3, 7, 10, 11], sorted(list(motion.morphs["B"].keys())))
        self.assertEqual(20, motion.morphs["B"][0].ratio)
        self.assertEqual(43, motion.morphs["B"][1].ratio)
        self.assertEqual(5, motion.morphs["B"][2].ratio)
        self.assertEqual(60, motion.morphs["B"][3].ratio)
        self.assertEqual(4, motion.morphs["B"][7].ratio)
        self.assertEqual(6, motion.morphs["B"][10].ratio)
        self.assertEqual(2, motion.morphs["B"][11].ratio)

    def test_replace_morph_05(self):
        motion = VmdMotion()
        motion.morphs["A"] = {}
        for fno, ratio in [(0, 10), (1, 20), (3, 30), (7, 0), (10, 3)]:
            motion.morphs["A"][fno] = VmdMorphFrame(fno)
            motion.morphs["A"][fno].ratio = ratio

        motion.morphs["B"] = {}
        for fno, ratio in [(1, 3), (2, 5), (7, 4), (11, 2)]:
            motion.morphs["B"][fno] = VmdMorphFrame(fno)
            motion.morphs["B"][fno].ratio = ratio

        morph_list = [("A", "B", 2), ("B", "C", 2)]

        data_set = MOptionsDataSet(motion, None, None, None, False, False, morph_list, None, None)

        service = MorphService(None)
        service.replace_morph(0, data_set)

        self.assertEqual(["B", "C"], list(motion.morphs.keys()))

        self.assertTrue("B" in motion.morphs)
        self.assertEqual([0, 1, 2, 3, 7, 10, 11], sorted(list(motion.morphs["B"].keys())))
        self.assertEqual(20, motion.morphs["B"][0].ratio)
        self.assertEqual(43, motion.morphs["B"][1].ratio)
        self.assertEqual(5, motion.morphs["B"][2].ratio)
        self.assertEqual(60, motion.morphs["B"][3].ratio)
        self.assertEqual(4, motion.morphs["B"][7].ratio)
        self.assertEqual(6, motion.morphs["B"][10].ratio)
        self.assertEqual(2, motion.morphs["B"][11].ratio)

        self.assertTrue("C" in motion.morphs)
        self.assertEqual([1, 2, 7, 11], sorted(list(motion.morphs["C"].keys())))
        self.assertEqual(6, motion.morphs["C"][1].ratio)
        self.assertEqual(10, motion.morphs["C"][2].ratio)
        self.assertEqual(8, motion.morphs["C"][7].ratio)
        self.assertEqual(4, motion.morphs["C"][11].ratio)

    def test_replace_morph_06(self):
        motion = VmdMotion()
        motion.morphs["A"] = {}
        for fno, ratio in [(0, 10), (1, 20), (3, 30), (7, 0), (10, 3)]:
            motion.morphs["A"][fno] = VmdMorphFrame(fno)
            motion.morphs["A"][fno].ratio = ratio

        motion.morphs["B"] = {}
        for fno, ratio in [(1, 3), (2, 5), (7, 4), (11, 2)]:
            motion.morphs["B"][fno] = VmdMorphFrame(fno)
            motion.morphs["B"][fno].ratio = ratio

        motion.morphs["C"] = {}
        for fno, ratio in [(5, 3), (7, 4), (8, 5)]:
            motion.morphs["C"][fno] = VmdMorphFrame(fno)
            motion.morphs["C"][fno].ratio = ratio

        morph_list = [("A", "B", 2), ("B", "C", 2)]

        data_set = MOptionsDataSet(motion, None, None, None, False, False, morph_list, None, None)

        service = MorphService(None)
        service.replace_morph(0, data_set)

        self.assertEqual(["B", "C"], sorted(list(motion.morphs.keys())))

        self.assertTrue("B" in motion.morphs)
        self.assertEqual([0, 1, 2, 3, 7, 10, 11], sorted(list(motion.morphs["B"].keys())))
        self.assertEqual(20, motion.morphs["B"][0].ratio)
        self.assertEqual(43, motion.morphs["B"][1].ratio)
        self.assertEqual(5, motion.morphs["B"][2].ratio)
        self.assertEqual(60, motion.morphs["B"][3].ratio)
        self.assertEqual(4, motion.morphs["B"][7].ratio)
        self.assertEqual(6, motion.morphs["B"][10].ratio)
        self.assertEqual(2, motion.morphs["B"][11].ratio)

        self.assertTrue("C" in motion.morphs)
        self.assertEqual([1, 2, 5, 7, 8, 11], sorted(list(motion.morphs["C"].keys())))
        self.assertEqual(6, motion.morphs["C"][1].ratio)
        self.assertEqual(10, motion.morphs["C"][2].ratio)
        self.assertEqual(3, motion.morphs["C"][5].ratio)
        self.assertEqual(12, motion.morphs["C"][7].ratio)
        self.assertEqual(4, motion.morphs["C"][11].ratio)

    def test_replace_morph_07(self):
        motion = VmdMotion()
        motion.morphs["A"] = {}
        for fno, ratio in [(0, 10), (1, 20), (3, 30), (7, 0), (10, 3)]:
            motion.morphs["A"][fno] = VmdMorphFrame(fno)
            motion.morphs["A"][fno].ratio = ratio

        motion.morphs["B"] = {}
        for fno, ratio in [(1, 3), (2, 5), (7, 4), (11, 2)]:
            motion.morphs["B"][fno] = VmdMorphFrame(fno)
            motion.morphs["B"][fno].ratio = ratio

        motion.morphs["C"] = {}
        for fno, ratio in [(5, 3), (7, 4), (8, 5)]:
            motion.morphs["C"][fno] = VmdMorphFrame(fno)
            motion.morphs["C"][fno].ratio = ratio

        morph_list = [("A", "A", 1), ("A", "D", 0.2)]

        data_set = MOptionsDataSet(motion, None, None, None, False, False, morph_list, None, None)

        service = MorphService(None)
        service.replace_morph(0, data_set)

        self.assertEqual(["A", "B", "C", "D"], sorted(list(motion.morphs.keys())))

        self.assertTrue("A" in motion.morphs)
        self.assertEqual([0, 1, 3, 7, 10], sorted(list(motion.morphs["A"].keys())))
        self.assertAlmostEqual(10, motion.morphs["A"][0].ratio)
        self.assertAlmostEqual(20, motion.morphs["A"][1].ratio)
        self.assertAlmostEqual(30, motion.morphs["A"][3].ratio)
        self.assertAlmostEqual(0, motion.morphs["A"][7].ratio)
        self.assertAlmostEqual(3, motion.morphs["A"][10].ratio)

        self.assertTrue("D" in motion.morphs)
        self.assertEqual([0, 1, 3, 7, 10], sorted(list(motion.morphs["D"].keys())))
        self.assertAlmostEqual(2, motion.morphs["D"][0].ratio)
        self.assertAlmostEqual(4, motion.morphs["D"][1].ratio)
        self.assertAlmostEqual(6, motion.morphs["D"][3].ratio)
        self.assertAlmostEqual(0, motion.morphs["D"][7].ratio)
        self.assertAlmostEqual(0.6, motion.morphs["D"][10].ratio)


class StanceServiceTest(unittest.TestCase):

    def test_stance_shoulder_01(self):
        arm_slope = MVector3D(-1.837494969367981, 18.923479080200195, 0.4923856854438782)
        shoulder_slope = MVector3D(-0.8141360282897949, 19.6701602935791, 0.4931679964065552)
        neck_base = MVector3D(0.0, 18.923479080200195, 0.4923856854438782)

        # 傾きパターン
        test_slope_param = [arm_slope, shoulder_slope, neck_base]
        slope_test_params = list(itertools.product(test_slope_param, repeat=2))
        # random.shuffle(slope_test_params)

        # 数値パターン
        test_number_param = [0, -1, 1]
        number_test_params = list(itertools.product(test_number_param, repeat=3))
        # random.shuffle(number_test_params)

        target_test_params = list(itertools.product(slope_test_params, number_test_params))

        for param in target_test_params:
            print("------------------")
            print("param[0][0]: %s" % param[0][0])
            print("param[0][1]: %s" % param[0][1])
            print("param[1][0]: %s" % param[1][0])
            print("param[1][1]: %s" % param[1][1])
            print("param[1][2]: %s" % param[1][2])
            rep_shoulder_slope = (param[0][0] - param[0][1]).normalized()
            rep_shoulder_slope_up = MVector3D(param[1][0], param[1][1], param[1][2])
            rep_shoulder_slope_cross = MVector3D.crossProduct(rep_shoulder_slope, rep_shoulder_slope_up).normalized()
            
            rep_shoulder_initial_slope_qq = MQuaternion.fromDirection(rep_shoulder_slope, rep_shoulder_slope_cross)
            print("rep_shoulder_slope: %s" % rep_shoulder_slope)
            print("rep_shoulder_slope_up: %s" % rep_shoulder_slope_up)
            print("qq: %s" % rep_shoulder_initial_slope_qq.toEulerAngles())
        
        self.assertTrue(True)

    def not_test_stance_shoulder_02(self):
        motion = VmdReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Motion/_VMDサイジング/鳳仙花/鳳仙花mkmk髭切007bミュ第一_0-2000.vmd").read_data()
        model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/刀剣乱舞/107_髭切/髭切【刀ミュ】mkmk008d 刀剣乱舞/髭切【刀ミュ】mkmk008d/髭切【刀ミュ3】mkmk008d_鳳仙花.pmx").read_data()
        
        # 傾きパターン
        test_slope_param = ["arm_name", "shoulder_name", "首根元"]
        all_slope_test_params = list(itertools.product(test_slope_param, repeat=2))
        slope_test_params = [(x00, x01) for (x00, x01) in all_slope_test_params if x00 != x01]
        print(len(slope_test_params))

        # 数値パターン
        test_number_param = [0, -1, 1]
        all_number_test_params = list(itertools.product(test_number_param, repeat=3))
        number_test_params = [(x00, x01, x02) for (x00, x01, x02) in all_number_test_params if x00 == 0 or x01 == 0 or x02 == 0]
        print(len(number_test_params))

        target_test_params = list(itertools.product(slope_test_params, number_test_params))
        print(len(target_test_params))

        random.shuffle(target_test_params)

        for params in target_test_params:
            print(params)

            copy_motion = motion.copy()
            dataset = MOptionsDataSet(copy_motion, model, model, "", False, False)
            dataset.test_params = params

            options = MOptions("", "", [dataset])

            service = StanceService(options)
            service.adjust_shoulder_stance(0, dataset)

            print("stance: %s" % dataset.motion.bones["右肩"][1625].rotation.toEulerAngles())
            print("original: %s" % motion.bones["右肩"][1625].rotation.toEulerAngles())

        self.assertTrue(True)
        
    def not_test_stance_shoulder_03(self):
        motion = VmdReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Motion/_VMDサイジング/鳳仙花/鳳仙花mkmk髭切007bミュ第一_0-2000.vmd").read_data()
        model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/刀剣乱舞/107_髭切/髭切【刀ミュ】mkmk008d 刀剣乱舞/髭切【刀ミュ】mkmk008d/髭切【刀ミュ3】mkmk008d_鳳仙花.pmx").read_data()
        
        # 傾きパターン
        slope_test_params = [('arm_name', 'shoulder_name')]

        # 数値パターン
        test_number_param = [0, -1, 1]
        all_number_test_params = list(itertools.product(test_number_param, repeat=3))
        number_test_params = [(x00, x01, x02) for (x00, x01, x02) in all_number_test_params if x00 == 0 or x01 == 0 or x02 == 0]
        print(len(number_test_params))

        target_test_params = list(itertools.product(slope_test_params, number_test_params))
        print(len(target_test_params))

        for params in target_test_params:
            print(params)

            copy_motion = motion.copy()
            dataset = MOptionsDataSet(copy_motion, model, model, "", False, False)
            dataset.test_params = params

            options = MOptions("", "", [dataset])

            service = StanceService(options)
            service.adjust_shoulder_stance(0, dataset)

            print("stance: %s" % dataset.motion.bones["右肩"][1625].rotation.toEulerAngles())
            print("original: %s" % motion.bones["右肩"][1625].rotation.toEulerAngles())

        self.assertTrue(True)

    def not_test_stance_shoulder_04(self):
        motion = VmdReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Motion/_VMDサイジング/鳳仙花/鳳仙花mkmk髭切007bミュ第一_0-2000.vmd").read_data()
        model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/刀剣乱舞/107_髭切/髭切【刀ミュ】mkmk008d 刀剣乱舞/髭切【刀ミュ】mkmk008d/髭切【刀ミュ3】mkmk008d_鳳仙花.pmx").read_data()
        
        # 傾きパターン
        test_slope_param = ["arm_name", "shoulder_name", "首根元"]
        all_slope_test_params = list(itertools.product(test_slope_param, repeat=2))
        slope_test_params = [(x00, x01) for (x00, x01) in all_slope_test_params if x00 != x01]
        print(len(slope_test_params))

        target_test_params = list(itertools.product(slope_test_params, slope_test_params))
        print(len(target_test_params))

        for params in target_test_params:
            print(params)

            copy_motion = motion.copy()
            dataset = MOptionsDataSet(copy_motion, model, model, "", False, False)
            dataset.test_params = params

            options = MOptions("", "", [dataset])

            service = StanceService(options)
            service.adjust_shoulder_stance(0, dataset)

            print("stance: %s" % dataset.motion.bones["右肩"][1625].rotation.toEulerAngles())
            print("original: %s" % motion.bones["右肩"][1625].rotation.toEulerAngles())

        self.assertTrue(True)

    def not_test_stance_shoulder_05(self):
        motion = VmdReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Motion/_VMDサイジング/鳳仙花/鳳仙花mkmk髭切007bミュ第一_0-2000.vmd").read_data()
        model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/刀剣乱舞/107_髭切/髭切【刀ミュ】mkmk008d 刀剣乱舞/髭切【刀ミュ】mkmk008d/髭切【刀ミュ3】mkmk008d_鳳仙花.pmx").read_data()
        
        # 傾きパターン
        test_slope_param = ["arm_name", "shoulder_name", "首根元"]
        all_slope_test_params = list(itertools.product(test_slope_param, repeat=2))
        slope_test_params = [(x00, x01) for (x00, x01) in all_slope_test_params if x00 != x01]

        # qqパターン
        test_qq_param = ["qq1", "qq1i", "qq2", "qq2i", "qq3", "qq3i", "0"]

        target_test_params = list(itertools.product(slope_test_params, test_qq_param))
        print(len(target_test_params))

        random.shuffle(target_test_params)

        for params in target_test_params:
            print(params)

            copy_motion = motion.copy()
            dataset = MOptionsDataSet(copy_motion, model, model, "", False, False)
            dataset.test_params = params

            options = MOptions("", "", [dataset])

            service = StanceService(options)
            service.adjust_shoulder_stance(0, dataset)

            print("stance: %s" % dataset.motion.bones["右肩"][1625].rotation.toEulerAngles())
            print("original: %s" % motion.bones["右肩"][1625].rotation.toEulerAngles())

        self.assertTrue(True)

    def not_test_stance_shoulder_06(self):
        new_rep_to_pos = MVector3D(16.638640587237887, 19.455697325211673, 4.067013732312591)
        rep_base_pos = MVector3D(15.527995423468052, 19.158781645638516, 2.353690174209908)
        up_pos = MVector3D(0.02597404821369409, -0.6341368197928823, 0.7727844735774392)
        parent_qq = MQuaternion.fromEulerAngles(4.444080622855673, 131.6889133202979, -6.602768822699441)

        arm_pos = MVector3D(-1.837494969367981, 18.923479080200195, 0.4923856854438782)
        shoulder_pos = MVector3D(-0.8141360282897949, 19.6701602935791, 0.4931679964065552)
        neck_base_pos = MVector3D(0.0, 19.6701602935791, 0.4931679517030716)

        # stance_shoulder2neck_qq = MQuaternion.fromEulerAngles(0.015789129707102025, -0.040575112727633096, 42.52534119964952)
        # stance_shoulder2arm_qq = MQuaternion.fromEulerAngles(0.011536139571057251, 0.03538278693844499, -36.1158910081693)

        # 傾きパターン
        test_slope_param = [arm_pos, shoulder_pos, neck_base_pos]
        all_slope_test_params = list(itertools.product(test_slope_param, repeat=2))
        slope_test_params = [(x00, x01) for (x00, x01) in all_slope_test_params if x00 != x01]

        # 数値パターン
        test_number_param = [0, -1, 1]
        all_number_test_params = list(itertools.product(test_number_param, repeat=3))
        number_test_params = [(x00, x01, x02) for (x00, x01, x02) in all_number_test_params if x00 == 0 or x01 == 0 or x02 == 0]

        # qqパターン
        # test_qq_param = [stance_shoulder2neck_qq, stance_shoulder2neck_qq.inverted(), stance_shoulder2arm_qq, stance_shoulder2arm_qq.inverted(), MQuaternion()]
        test_qq_param = [MQuaternion()]

        target_test_params = list(itertools.product(slope_test_params, number_test_params, test_qq_param))
        print(len(target_test_params))

        random.shuffle(target_test_params)

        for params in target_test_params:
            print("-----------------------")
            print(params[0][0])
            print(params[0][1])
            print(params[1])
            print(params[2].toEulerAngles())

            rep_shoulder_slope = (params[0][0] - params[0][1]).normalized()
            print("rep_shoulder_slope: %s" % rep_shoulder_slope)

            rep_shoulder_slope_up = MVector3D(params[1][0], params[1][1], params[1][2])
            print("rep_shoulder_slope_up: %s" % rep_shoulder_slope_up)

            initial = MQuaternion.fromDirection(rep_shoulder_slope, rep_shoulder_slope_up)
            print("initial: %s" % initial.toEulerAngles())

            direction = new_rep_to_pos - rep_base_pos
            up = MVector3D.crossProduct(direction, up_pos)
            from_orientation = MQuaternion.fromDirection(direction.normalized(), up.normalized())

            from_rotation = parent_qq.inverted() * from_orientation * initial.inverted() * params[2]
            from_rotation.normalize()
            print("rot %s" % from_rotation.toEulerAngles4MMD())

    def not_test_stance_shoulder_07(self):
        new_rep_to_pos = MVector3D(16.638640587237894, 19.455697325211673, 4.067013732312591)
        rep_base_pos = MVector3D(15.541596036361701, 18.419343683301417, 2.4565491530944494)
        up_pos = MVector3D(-0.13131308583164614, -0.017769852724240698, 0.10088527183640322)
        parent_qq = MQuaternion.fromEulerAngles(4.444080622855673, 131.6889133202979, -6.602768822699441)

        arm_pos = MVector3D(-1.837494969367981, 18.923479080200195, 0.4923856854438782)
        shoulder_pos = MVector3D(-0.8141360282897949, 19.6701602935791, 0.4931679964065552)
        neck_base_pos = MVector3D(0.0, 18.923479080200195, 0.4923856854438782)
        another_arm_pos = MVector3D(1.837494969367981, 18.923479080200195, 0.4923856854438782)
        another_shoulder_pos = MVector3D(0.8141360282897949, 19.6701602935791, 0.493167906999588)

        # 傾きパターン
        test_slope_param = [arm_pos, shoulder_pos, neck_base_pos]
        all_slope_test_params = list(itertools.product(test_slope_param, repeat=2))
        slope_test_params = [(x00, x01) for (x00, x01) in all_slope_test_params if x00 != x01]

        # upパターン
        test_up_param = [arm_pos, shoulder_pos, neck_base_pos, another_arm_pos, another_shoulder_pos]
        all_up_test_params = list(itertools.product(test_up_param, repeat=2))
        up_test_params = [(x00, x01) for (x00, x01) in all_up_test_params if x00 != x01]

        # 数値パターン
        test_number_param = [0, -1, 1]
        all_number_test_params = list(itertools.product(test_number_param, repeat=3))
        number_test_params = [(x00, x01, x02) for (x00, x01, x02) in all_number_test_params if x00 == 0 or x01 == 0 or x02 == 0]

        target_test_params = list(itertools.product(slope_test_params, number_test_params, up_test_params))
        print(len(target_test_params))

        random.shuffle(target_test_params)

        for params in target_test_params:
            print("-----------------------")
            print(params[0][0])
            print(params[0][1])
            print(params[1])
            print(params[2][0])
            print(params[2][1])

            rep_shoulder_slope = (params[0][0] - params[0][1]).normalized()
            print("rep_shoulder_slope: %s" % rep_shoulder_slope)

            rep_shoulder_slope_up = MVector3D(params[1][0], params[1][1], params[1][2])
            print("rep_shoulder_slope_up: %s" % rep_shoulder_slope_up)

            rep_shoulder_up = (params[2][0] - params[2][1]).normalized()
            print("rep_shoulder_slope: %s" % rep_shoulder_slope)

            shoulder_cross = MVector3D.crossProduct(rep_shoulder_slope_up, rep_shoulder_up).normalized()
            print("shoulder_cross: %s" % shoulder_cross)

            initial = MQuaternion.fromDirection(rep_shoulder_slope, rep_shoulder_up)
            print("initial: %s" % initial.toEulerAngles())

            direction = new_rep_to_pos - rep_base_pos
            up = MVector3D.crossProduct(direction, up_pos)
            from_orientation = MQuaternion.fromDirection(direction.normalized(), up.normalized())

            from_rotation = parent_qq.inverted() * from_orientation * initial.inverted()
            from_rotation.normalize()
            print("rot %s" % from_rotation.toEulerAngles4MMD())
            print("original: %s" % MVector3D(21.338723875696445, 15.845333083479046, 37.954108757721826))

    def not_test_stance_shoulder_08(self):
        new_rep_to_pos = MVector3D(16.638640587237894, 19.455697325211673, 4.067013732312591)
        # rep_base_pos = MVector3D(15.541596036361701, 18.419343683301417, 2.4565491530944494)
        rep_from_pos = MVector3D(16.07129122417615, 19.252113744303983, 2.952803072461259)
        up_pos = MVector3D(0.02597404821369409, -0.6341368197928823, 0.7727844735774392)
        parent_qq = MQuaternion.fromEulerAngles(4.444080622855673, 131.6889133202979, -6.602768822699441)

        arm_pos = MVector3D(-1.837494969367981, 18.923479080200195, 0.4923856854438782)
        shoulder_pos = MVector3D(-0.8141360282897949, 19.6701602935791, 0.4931679964065552)
        neck_base_pos = MVector3D(0.0, 18.923479080200195, 0.4923856854438782)
        another_arm_pos = MVector3D(1.837494969367981, 18.923479080200195, 0.4923856854438782)
        another_shoulder_pos = MVector3D(0.8141360282897949, 19.6701602935791, 0.493167906999588)

        # 傾きパターン
        test_slope_param = [arm_pos, shoulder_pos, neck_base_pos]
        all_slope_test_params = list(itertools.product(test_slope_param, repeat=2))
        slope_test_params = [(x00, x01) for (x00, x01) in all_slope_test_params if x00 != x01]

        # upパターン
        test_up_param = [arm_pos, shoulder_pos, neck_base_pos, another_arm_pos, another_shoulder_pos]
        all_up_test_params = list(itertools.product(test_up_param, repeat=2))
        up_test_params = [(x00, x01) for (x00, x01) in all_up_test_params if x00 != x01]

        # 数値パターン
        test_number_param = [0, -1, 1]
        all_number_test_params = list(itertools.product(test_number_param, repeat=3))
        number_test_params = [(x00, x01, x02) for (x00, x01, x02) in all_number_test_params if x00 == 0 or x01 == 0 or x02 == 0]

        target_test_params = list(itertools.product(slope_test_params, number_test_params, up_test_params))
        print(len(target_test_params))

        random.shuffle(target_test_params)

        for params in target_test_params:
            print("-----------------------")
            print(params[0][0])
            print(params[0][1])
            print(params[1])
            print(params[2][0])
            print(params[2][1])

            rep_shoulder_slope = (params[0][0] - params[0][1]).normalized()
            print("rep_shoulder_slope: %s" % rep_shoulder_slope)

            rep_shoulder_slope_up = MVector3D(params[1][0], params[1][1], params[1][2])
            print("rep_shoulder_slope_up: %s" % rep_shoulder_slope_up)

            shoulder_cross = MVector3D.crossProduct(rep_shoulder_slope, rep_shoulder_slope_up).normalized()
            print("shoulder_cross: %s" % shoulder_cross)

            initial = MQuaternion.fromDirection(rep_shoulder_slope, shoulder_cross)
            print("initial: %s" % initial.toEulerAngles())

            direction = new_rep_to_pos - rep_from_pos
            up = MVector3D.crossProduct(direction, up_pos)
            from_orientation = MQuaternion.fromDirection(direction.normalized(), up.normalized())

            from_rotation = parent_qq.inverted() * from_orientation * initial.inverted()
            from_rotation.normalize()
            print("rot %s" % from_rotation.toEulerAngles4MMD())
            print("original: %s" % MVector3D(21.338723875696445, 15.845333083479046, 37.954108757721826))

    def test_stance_shoulder_09(self):
        # motion = VmdReader("E:/MMD/MikuMikuDance_v926x64/Work/202001_sizing/肩/折岸みつ肩2.vmd").read_data()
        # org_model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/オリジナル/折岸みつ つみだんご/折岸みつ.pmx").read_data()
        # rep_model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/刀剣乱舞/055_鶯丸/鶯丸 さばそ式ver1.75配布用/さばそ式鶯丸(通常・刀無)ver1.75.pmx").read_data()
        motion = VmdReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Motion/運動/バレエっぽいターン グレイ/バレエっぽいターン.vmd").read_data()
        org_model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/VOCALOID/初音ミク/あぴミク01_Ver.1.04 アレン・ベルル/Appearance Miku_01_Ver.1.04_準標準.pmx").read_data()
        rep_model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/VOCALOID/初音ミク/底辺508式初音ミク_素足モデル せんと(鈍棒P)/miku_v3(素足_袖なし).pmx").read_data()

        # 数値パターン
        test_number_param = [0, -1, 1]
        all_number_test_params = list(itertools.product(test_number_param, repeat=3))
        number_test_params = [(x00, x01, x02) for (x00, x01, x02) in all_number_test_params if x00 == 0 or x01 == 0 or x02 == 0]
        print(len(number_test_params))

        for params in number_test_params:
            print(params)

            copy_motion = motion.copy()
            dataset = MOptionsDataSet(copy_motion, org_model, rep_model, "", True, False, [])
            dataset.test_params = params

            options = MOptions("", "", [dataset], None, None, False, None)

            service = StanceService(options)
            service.adjust_shoulder_stance(0, dataset)

            print("right stance: %s" % dataset.motion.bones["右肩"][0].rotation.toEulerAngles())
            print("right original: %s" % motion.bones["右肩"][0].rotation.toEulerAngles())
            print("left stance: %s" % dataset.motion.bones["左肩"][0].rotation.toEulerAngles())
            print("left original: %s" % motion.bones["左肩"][0].rotation.toEulerAngles())

            pass

        self.assertTrue(True)

    def not_test_adjust_upper_stance01(self):
        motion = VmdReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Motion/運動/バレエっぽいターン グレイ/バレエっぽいターン.vmd").read_data()
        org_model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/VOCALOID/初音ミク/あぴミク01_Ver.1.04 アレン・ベルル/Appearance Miku_01_Ver.1.04_準標準.pmx").read_data()
        rep_model = PmxReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Model/VOCALOID/初音ミク/底辺508式初音ミク_素足モデル せんと(鈍棒P)/miku_v3(素足_袖なし).pmx").read_data()

        # 数値パターン
        test_number_param = [0, -1, 1]
        all_number_test_params = list(itertools.product(test_number_param, repeat=3))
        number_test_params = [(x00, x01, x02) for (x00, x01, x02) in all_number_test_params if x00 == 0 or x01 == 0 or x02 == 0]
        print(len(number_test_params))

        for params in number_test_params:
            print(params)

            copy_motion = motion.copy()
            dataset = MOptionsDataSet(copy_motion, org_model, rep_model, "", True, False, [])
            dataset.test_params = params

            options = MOptions("", "", [dataset], None, None, False, None)

            service = StanceService(options)
            service.adjust_upper_stance(0, dataset)

            print("stance: %s" % dataset.motion.bones["上半身"][44].rotation.toEulerAngles())
            print("original: %s" % motion.bones["上半身"][44].rotation.toEulerAngles())
            print("original: %s" % motion.bones["上半身"][0].rotation.toEulerAngles())

        self.assertTrue(True)



if __name__ == "__main__":
    unittest.main()

