import os

pkgs = [
    "curl",
    "libevent",
    "libmaxminddb",
    "libressl",
    "measurement-kit"
]

arch_map = {
    "x86_64": "amd64",
}

plat_map = {
    "macos": "darwin",
    "mingw": "windows",
    "linux": "linux"
}

def print_cgo_line_include(platform, pkg_name, arch):
    pkg_root = os.path.join("libs", "MK_DIST", platform, pkg_name)
    versions = list(filter(lambda x: x != ".DS_Store", os.listdir(pkg_root)))
    version = versions[0]
    includepath = os.path.join(pkg_root, version, arch, "include")
    line = "// #cgo {plat},{arch} CFLAGS: -I${{SRCDIR}}/{includepath}".format(plat=plat_map[platform], arch=arch_map[arch],includepath=includepath)
    print(line)

def print_cgo_line_lib(platform, pkg_name, arch):
    pkg_root = os.path.join("libs", "MK_DIST", platform, pkg_name)
    versions = list(filter(lambda x: x != ".DS_Store", os.listdir(pkg_root)))
    assert len(versions) == 1, "Duplicate versions. Try cleaning libs"
    version = versions[0]
    lib_root = os.path.join(pkg_root, version, arch, "lib")
    lib_names = os.listdir(lib_root)

    for lib_name in lib_names:
        libpath = os.path.join(lib_root, lib_name)
        line = "// #cgo {plat},{arch} LDFLAGS: ${{SRCDIR}}/{libpath}".format(plat=plat_map[platform], arch=arch_map[arch],libpath=libpath)
        print(line)

def main():
    for platform in plat_map.keys():
        print_cgo_line_include(platform, "measurement-kit", "x86_64")
        for pkg in pkgs:
            print_cgo_line_lib(platform, pkg, "x86_64")
        print("\n\n")

if __name__ == "__main__":
    main()
