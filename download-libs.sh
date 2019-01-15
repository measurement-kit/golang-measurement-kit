#!/bin/bash
set -e
TARGET_PLATFORM="all"
LIBS_VERSION="0.2.0"
LIBS_SHASUM=$(cat <<-END
8430f6e9a77c7195b1147dee4984221c3484c1660ea86088e930610cd6c97f5d  macos-curl-7.63.0+2.tar.gz
550d3f6ba10507974b5af55983a6e5e4203fc7ba26f6fca65081bf9721804048  macos-libevent-2.1.8+4.tar.gz
b77999ca0f59ed87cc7fa9b0a2dba830caa358531f0dd2f6e94a1490a3d2435b  macos-libmaxminddb-1.3.2+3.tar.gz
280b48744301f36f1a3274a0ea9da7ff7dd60d3de779d037407b529522655654  macos-libressl-2.8.3+1.tar.gz
6aa3d90fc32b98fd7e4524da7aec28bb9d228c6e7228129ed11071bf1c50c732  macos-measurement-kit-0.9.1+1.tar.gz
23732911ed0406ef4753af0e2e0a4ceae39d1eb94ca6247291759e82e76a4cea  mingw-curl-7.63.0+2.tar.gz
b1d25568e5f2d00647dcef58a4dd06d717b1001980b1c092e9a3bc55b393e559  mingw-libevent-2.1.8+4.tar.gz
2b17a7769cd5e70172ad9ae1374eab9f7fec01e13567b40f1d0b252ff3588f95  mingw-libmaxminddb-1.3.2+3.tar.gz
7c62fae040b242ffa3de5fc4635de69ac440af2b4401b016fc0e197c7abe3962  mingw-libressl-2.8.3+1.tar.gz
8cad84a3253b14377384148163eccf1c26765a65d3c4487d47726b9a08a9bbc7  mingw-measurement-kit-0.9.1+1.tar.gz
END
)

PKG_TOPDIR=$(cd $(dirname $0) && pwd -P)

download_libs()
{
    PLATFORM=$1
    IFS=$'\n'
    echo "Downloading libs for $PLATFORM"

    mkdir -p $PKG_TOPDIR/libs
    cd $PKG_TOPDIR/libs

    for lib in $(echo "$LIBS_SHASUM" | grep " $1-");do
        SHASUM=$(echo $lib | awk '{ print $1 }')
        PKG_NAME=$(echo $lib | awk '{ print $2 }')
        DOWNLOAD_URL="https://github.com/measurement-kit/script-build-unix/releases/download/v${LIBS_VERSION}/$PKG_NAME"

        echo "  downloading $DOWNLOAD_URL into $PKG_TOPDIR/libs"
        curl -LsO $DOWNLOAD_URL

        REAL_CHECKSUM=`shasum -a 256 $PKG_NAME | awk '{print $1}'`
        [ "$REAL_CHECKSUM" = "$SHASUM" ]

        tar xzf $PKG_NAME
        rm $PKG_NAME
    done
    unset IFS
}

if [ "$1" != "" ];then
    TARGET_PLATFORM=$1
fi

mkdir -p $PKG_TOPDIR/libs
if [ "$TARGET_PLATFORM" == "all" ];then
    download_libs macos
    download_libs mingw
    download_libs linux
    download_libs linux_armv7
elif [ "$TARGET_PLATFORM" == "macos" ];then
    download_libs macos
elif [ "$TARGET_PLATFORM" == "linux" ];then
    download_libs linux
elif [ "$TARGET_PLATFORM" == "linux_armv7" ];then
    download_libs linux_armv7
elif [ "$TARGET_PLATFORM" == "mingw" ];then
    download_libs mingw
else
    echo "Error: Unsupported platform $TARGET_PLATFORM"
    exit 1
fi
exit 0
