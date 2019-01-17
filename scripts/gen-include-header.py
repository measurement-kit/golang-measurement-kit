import os
from glob import glob

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

tmpl = """// #cgo {platform},{arch} CFLAGS: -I${{SRCDIR}}/libs/MK_DIST/{mk_platform}/measurement-kit/{measurement_kit_version}/{mk_arch}/include
// #cgo {platform},{arch} LDFLAGS: ${{SRCDIR}}/libs/MK_DIST/{mk_platform}/measurement-kit/{measurement_kit_version}/{mk_arch}/lib/libmeasurement_kit.a
// #cgo {platform},{arch} LDFLAGS: ${{SRCDIR}}/libs/MK_DIST/{mk_platform}/libmaxminddb/{libmaxminddb_version}/{mk_arch}/lib/libmaxminddb.a
// #cgo {platform},{arch} LDFLAGS: ${{SRCDIR}}/libs/MK_DIST/{mk_platform}/curl/{curl_version}/{mk_arch}/lib/libcurl.a
// #cgo {platform},{arch} LDFLAGS: ${{SRCDIR}}/libs/MK_DIST/{mk_platform}/libevent/{libevent_version}/{mk_arch}/lib/libevent_openssl.a
// #cgo {platform},{arch} LDFLAGS: ${{SRCDIR}}/libs/MK_DIST/{mk_platform}/libressl/{libressl_version}/{mk_arch}/lib/libssl.a
// #cgo {platform},{arch} LDFLAGS: ${{SRCDIR}}/libs/MK_DIST/{mk_platform}/libressl/{libressl_version}/{mk_arch}/lib/libcrypto.a
// #cgo {platform},{arch} LDFLAGS: ${{SRCDIR}}/libs/MK_DIST/{mk_platform}/libevent/{libevent_version}/{mk_arch}/lib/libevent_core.a
// #cgo {platform},{arch} LDFLAGS: ${{SRCDIR}}/libs/MK_DIST/{mk_platform}/libevent/{libevent_version}/{mk_arch}/lib/libevent_extra.a
// #cgo {platform},{arch} LDFLAGS: ${{SRCDIR}}/libs/MK_DIST/{mk_platform}/libevent/{libevent_version}/{mk_arch}/lib/libevent_pthreads.a"""

def get_package_versions():
    pkg_versions = {}

    plat_root = glob('libs/MK_DIST/*')[0]
    pkgs_paths = glob(os.path.join(plat_root, '*'))
    for pkg_path in pkgs_paths:
        pkg_name = os.path.basename(pkg_path)
        versions = list(filter(lambda x: x != ".DS_Store", os.listdir(pkg_path)))
        assert len(versions) == 1
        pkg_versions[pkg_name.replace('-', '_') + '_version'] = versions[0]
    return pkg_versions

def get_special_cgo_lines(arch, platform):
    if platform == "windows" and arch == "amd64":
        return """// #cgo windows LDFLAGS: -static
// #cgo windows,amd64 LDFLAGS: -lws2_32"""

    if platform == "linux" and arch == "amd64":
        return "// #cgo linux,amd64 LDFLAGS: -lm"

def main():
    package_versions = get_package_versions()
    for mk_arch, arch in arch_map.items():
        for mk_platform, platform in plat_map.items():
            line = get_special_cgo_lines(arch, platform)
            if line:
                print(line)
            print(tmpl.format(
                mk_platform=mk_platform,
                platform=platform,
                mk_arch=mk_arch,
                arch=arch,
                **package_versions
            ))
            print("//")

if __name__ == "__main__":
    main()
