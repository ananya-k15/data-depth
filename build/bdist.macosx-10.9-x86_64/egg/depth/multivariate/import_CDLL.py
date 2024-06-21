import ctypes as ct
import sys, os, glob


def import_CDLL():
    ddalpha_exact, ddalpha_approx = None, None
    if sys.platform == "linux" or sys.platform == "darwin":
        for i in sys.path:
            if i.split("/")[-1] in ["site-packages", "dist-packages"]:
                ddalpha_exact = glob.glob(i + "/*ddalpha*.so")
                ddalpha_approx = glob.glob(i + "/*depth_wrapper*.so")
                if ddalpha_exact and ddalpha_approx:
                    break

        # Add additional paths to search for arm64
        if not (ddalpha_exact and ddalpha_approx):
            ddalpha_exact = glob.glob("build/lib.macosx-10.9-x86_64-3.10/*ddalpha*.so")
            ddalpha_approx = glob.glob(
                "build/lib.macosx-10.9-x86_64-3.10/*depth_wrapper*.so"
            )
            if not (ddalpha_exact and ddalpha_approx):
                ddalpha_exact = glob.glob(
                    "build/lib.macosx-10.9-x86_64-3.9/*ddalpha*.so"
                )
                ddalpha_approx = glob.glob(
                    "build/lib.macosx-10.9-x86_64-3.9/*depth_wrapper*.so"
                )

        print(f"Found ddalpha_exact: {ddalpha_exact}")
        print(f"Found ddalpha_approx: {ddalpha_approx}")
        if ddalpha_exact and ddalpha_approx:
            libr = ct.CDLL(ddalpha_exact[0])
            libRom = ct.CDLL(ddalpha_approx[0])
        else:
            raise FileNotFoundError("Shared libraries not found")
    elif sys.platform == "win32":
        site_packages = [
            p for p in sys.path if "site-packages" in p or "dist-packages" in p
        ]
        for i in site_packages:
            os.add_dll_directory(i)
            ddalpha_exact = glob.glob(i + "/depth/src/*ddalpha*.dll")
            ddalpha_approx = glob.glob(i + "/depth/src/*depth_wrapper*.dll")
            if ddalpha_exact and ddalpha_approx:
                break
        print(f"Found ddalpha_exact: {ddalpha_exact}")
        print(f"Found ddalpha_approx: {ddalpha_approx}")
        if ddalpha_exact and ddalpha_approx:
            libr = ct.CDLL(ddalpha_exact[0])
            libRom = ct.CDLL(ddalpha_approx[0])
        else:
            raise FileNotFoundError("Shared libraries not found")
    else:
        raise OSError("Unsupported platform")
    return libr, libRom


libr, libRom = import_CDLL()


# import ctypes as ct
# import multiprocessing as mp
# import sys, os, glob


# def import_CDLL():
#     if sys.platform == "linux":
#         for i in sys.path:
#             if (
#                 i.split("/")[-1] == "site-packages"
#                 or i.split("/")[-1] == "dist-packages"
#             ):  # Add search dist-packages
#                 de = glob.glob(i + "/*ddalpha*.so")
#                 da = glob.glob(i + "/*depth_wrapper*.so")
#                 if da != [] and de != []:
#                     ddalpha_exact = glob.glob(i + "/*ddalpha*.so")
#                     ddalpha_approx = glob.glob(i + "/*depth_wrapper*.so")
#                 else:
#                     print(da, de)
#         libr = ct.CDLL(ddalpha_exact[0])
#         libRom = ct.CDLL(ddalpha_approx[0])

#     if sys.platform == "darwin":
#         # for i in sys.path:
#         #     if (
#         #         i.split("/")[-1] == "site-packages"
#         #         or i.split("/")[-1] == "dist-packages"
#         #     ):  # Find path - ANANYA
#         #         print(i)
#         #         # Add search dist-packages
#         #         de = glob.glob(i + "/*ddalpha*.so")
#         #         da = glob.glob(os.path.expanduser(i) + "/*depth_wrapper*.so")
#         #         print(de, da)
#         #         if da != [] and de != []:
#         #             ddalpha_exact = glob.glob(i + "/*ddalpha*.so")
#         #             ddalpha_approx = glob.glob(i + "/*depth_wrapper*.so")

#         for i in sys.path:
#             if i.split("/")[-1] in ["site-packages", "dist-packages"]:
#                 ddalpha_exact = glob.glob(i + "/*ddalpha*.so")
#                 ddalpha_approx = glob.glob(i + "/*depth_wrapper*.so")
#                 if ddalpha_exact and ddalpha_approx:
#                     break

#         # Add additional paths to search
#         if not (ddalpha_exact and ddalpha_approx):
#             ddalpha_exact = glob.glob("build/lib.macosx-10.9-arm64-3.10/*ddalpha*.so")
#             ddalpha_approx = glob.glob(
#                 "build/lib.macosx-10.9-arm64-3.10/*depth_wrapper*.so"
#             )
#             if not (ddalpha_exact and ddalpha_approx):
#                 ddalpha_exact = glob.glob(
#                     "build/lib.macosx-10.9-arm64-3.9/*ddalpha*.so"
#                 )
#                 ddalpha_approx = glob.glob(
#                     "build/lib.macosx-10.9-arm64-3.9/*depth_wrapper*.so"
#                 )

#         print(f"Found ddalpha_exact: {ddalpha_exact}")
#         print(f"Found ddalpha_approx: {ddalpha_approx}")
#         if ddalpha_exact and ddalpha_approx:
#             libr = ct.CDLL(ddalpha_exact[0])
#             libRom = ct.CDLL(ddalpha_approx[0])
#         else:
#             raise FileNotFoundError("Shared libraries not found")

#         libr = ct.CDLL(ddalpha_exact[0])
#         libRom = ct.CDLL(ddalpha_approx[0])

#     if sys.platform == "win32":
#         site_packages = [
#             p for p in sys.path if ("site-packages" in p) or ("dist-packages" in p)
#         ]  # Add search dist-packages
#         for i in site_packages:
#             os.add_dll_directory(i)
#             ddalpha_exact = glob.glob(i + "/depth/src/*ddalpha*.dll")
#             ddalpha_approx = glob.glob(i + "/depth/src/*depth_wrapper*.dll")
#             if ddalpha_exact + ddalpha_approx != []:
#                 libr = ct.CDLL(r"" + ddalpha_exact[0])
#                 libRom = ct.CDLL(r"" + ddalpha_approx[0])
#     return libr, libRom


# libr, libRom = import_CDLL()
