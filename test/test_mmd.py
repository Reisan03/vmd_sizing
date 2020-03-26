# -*- coding: utf-8 -*-
#
import unittest
import sys
import pathlib
# このソースのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append(str(current_dir) + '/../')
sys.path.append(str(current_dir) + '/../src/')

from mmd.PmxReader import PmxReader # noqa
from mmd.VmdReader import VmdReader # noqa
from mmd.PmxData import PmxModel, Vertex, Material, Bone, Morph, DisplaySlot, RigidBody, Joint # noqa
from mmd.VmdData import VmdMotion, VmdBoneFrame, VmdCameraFrame, VmdInfoIk, VmdLightFrame, VmdMorphFrame, VmdShadowFrame, VmdShowIkFrame # noqa
from module.MMath import MRect, MVector2D, MVector3D, MVector4D, MQuaternion, MMatrix4x4 # noqa
from module.MOptions import MOptions # noqa
from module.MParams import BoneLinks # noqa
from utils import MBezierUtils # noqa
from utils.MException import SizingException # noqa
from utils.MLogger import MLogger # noqa

logger = MLogger(__name__, level=1)


class PmxDataTest(unittest.TestCase):

    def test_create_link_2_top_one_01(self):
        pmx_data = PmxModel()
        pmx_data.bones["SIZING_ROOT_BONE"] = Bone("SIZING_ROOT_BONE", "SIZING_ROOT_BONE", MVector3D(), -1, 0, 0)
        pmx_data.bones["SIZING_ROOT_BONE"].index = -1
        pmx_data.bones["右肩"] = Bone("右肩", None, MVector3D(), -1, 0, 0)
        pmx_data.bones["右肩"].index = 0

        with self.assertRaises(SizingException):
            links = pmx_data.create_link_2_top_one("右手首")

            print(links)

    def test_create_link_2_top_one_02(self):
        pmx_data = PmxModel()
        pmx_data.bones["SIZING_ROOT_BONE"] = Bone("SIZING_ROOT_BONE", "SIZING_ROOT_BONE", MVector3D(), -1, 0, 0)
        pmx_data.bones["SIZING_ROOT_BONE"].index = -1
        pmx_data.bones["右肩"] = Bone("右肩", None, MVector3D(), -1, 0, 0)
        pmx_data.bones["右肩"].index = 0
        pmx_data.bones["右手首"] = Bone("右手首", None, MVector3D(), -1, 0, 0)
        pmx_data.bones["右手首"].index = 1

        links = pmx_data.create_link_2_top_one("右手首")
        self.assertEqual(len(links.all()), 1)

    def test_create_link_2_top_one_03(self):
        pmx_data = PmxModel()
        pmx_data.bones["SIZING_ROOT_BONE"] = Bone("SIZING_ROOT_BONE", "SIZING_ROOT_BONE", MVector3D(), -1, 0, 0)
        pmx_data.bones["SIZING_ROOT_BONE"].index = -1
        pmx_data.bones["右肩"] = Bone("右肩", None, MVector3D(), -1, 0, 0)
        pmx_data.bones["右肩"].index = len(pmx_data.bones) - 1
        pmx_data.bones["右腕"] = Bone("右腕", None, MVector3D(), -1, 0, 0)
        pmx_data.bones["右腕"].index = len(pmx_data.bones) - 1
        pmx_data.bones["右ひじ"] = Bone("右ひじ", None, MVector3D(), -1, 0, 0)
        pmx_data.bones["右ひじ"].index = len(pmx_data.bones) - 1
        pmx_data.bones["右手首"] = Bone("右手首", None, MVector3D(), -1, 0, 0)
        pmx_data.bones["右手首"].index = len(pmx_data.bones) - 1
        pmx_data.bones["左腕"] = Bone("左腕", None, MVector3D(), -1, 0, 0)
        pmx_data.bones["左腕"].index = len(pmx_data.bones) - 1

        links = pmx_data.create_link_2_top_one("右手首")
        self.assertEqual(len(links.all()), 4)


class VmdDataTest(unittest.TestCase):

    def test_calc_bone_by_interpolation_01(self):
        motion = VmdReader("D:/MMD/MikuMikuDance_v926x64/UserFile/Motion/ダンス_1人/ドラマツルギー motion 配布用 moka/ドラマツルギー_0-500.vmd").read_data()
        
        bf = motion.calc_bone_by_interpolation("右腕", 101)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 27.1, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 16.2, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), -32.9, delta=0.1)

        bf = motion.calc_bone_by_interpolation("右腕", 143)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 32.2, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 57.3, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), -23.6, delta=0.1)

        bf = motion.calc_bone_by_interpolation("右腕", 107)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 27.2, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 16.7, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), -32.8, delta=0.1)

        bf = motion.calc_bone_by_interpolation("右腕", 121)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 28.6, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 24.5, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), -31.4, delta=0.1)

        bf = motion.calc_bone_by_interpolation("右腕", 137)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 32.1, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 55.2, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), -24.1, delta=0.1)

        bf = motion.calc_bone_by_interpolation("センター", 108)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 1.00, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 1.75, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0, delta=0.1)

        bf = motion.calc_bone_by_interpolation("センター", 143)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 1.20, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 1.90, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0, delta=0.1)

        bf = motion.calc_bone_by_interpolation("センター", 135)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 1.18, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 1.89, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0, delta=0.1)

        bf = motion.calc_bone_by_interpolation("センター", 340)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 3.21, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), -0.96, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0, delta=0.1)

        bf = motion.calc_bone_by_interpolation("右足ＩＫ", 417)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 2.75, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 2.92, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 2.19, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), -29.6, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), -25.2, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 5.0, delta=0.1)

        bf = motion.calc_bone_by_interpolation("左足ＩＫ", 420)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 2.47, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 2.28, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 1.39, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), -17.4, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 1.9, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.7, delta=0.1)

    def test_calc_bone_by_interpolation_02(self):
        motion = VmdReader(u"test/data/補間曲線テスト01.vmd").read_data()
        
        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 0)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 15)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 20, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 30, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 40, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 50, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 60.00003815, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 70, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 1)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0.032109514, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 10.18260956, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 4.065711975, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0.000829206, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.000238923, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.000410508, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 2)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0.140442505, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 12.61500168, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 8.287061691, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0.007236294, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.002085242, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.003582553, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 3)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0.348192513, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 13.84411716, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 12.79018593, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0.026710032, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.007699313, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.013225263, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 4)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 0.698622525, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 14.49679756, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 17.72015953, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0.069654942, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.020092424, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.034498487, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 5)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 1.264359236, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 14.82721519, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 23.55570602, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0.151426569, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.043738037, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.07503701, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 6)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 2.228799105, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 14.96385574, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 28.47421646, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0.293533772, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.084980235, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.145587772, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 7)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 4.250654697, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 14.99863911, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 29.97695541, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0.529829144, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.153979659, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.263184816, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 8)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 15.74932003, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 15.00131607, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 31.17938614, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 0.91197902, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.266692847, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.454135865, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 9)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 17.77118301, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 15.03609848, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 32.36212158, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 1.525828362, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.450684816, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 0.762894511, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 10)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 18.73562622, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 15.17386436, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 33.57285309, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 2.53502202, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 0.761205316, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 1.276175618, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 11)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 19.3013649, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 15.50316238, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 34.80752563, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 4.252967358, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 1.313556314, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 2.167253256, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 12)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 19.65179825, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 16.15584373, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 36.06707764, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 7.438279152, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 2.422097683, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 3.884207487, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 13)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 19.85955048, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 17.38496399, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 37.35407639, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 14.49954891, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 5.332914352, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 8.068556786, delta=0.1)

        bf = motion.calc_bone_by_interpolation("ﾎﾞｰﾝ01", 14)
        print(bf)
        self.assertAlmostEqual(bf.position.x(), 19.96788788, delta=0.1)
        self.assertAlmostEqual(bf.position.y(), 19.81736565, delta=0.1)
        self.assertAlmostEqual(bf.position.z(), 38.66796112, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().x(), 33.70291519, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().y(), 18.53442383, delta=0.1)
        self.assertAlmostEqual(bf.rotation.toEulerAngles4MMD().z(), 24.47537041, delta=0.1)



if __name__ == "__main__":
    unittest.main()
