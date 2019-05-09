# Go Measurement Kit

Measurement Kit bindings for go.

**Attention** this is work on progress and is highly unstable.

Do not use it for anything serious, for the moment.

## Getting started

### macOS

Install Measurement Kit using brew:

```bash
brew tap measurement-kit/measurement-kit
brew install measurement-kit
```

If you've already installed `measurement-kit`, do:

```bash
brew upgrade
```

to make sure you're on the latest released version.

Then you're all set. Just `go get -v ./...` as usual.

### Linux

We have a Docker container. Enter into the container with:

```bash
docker run -it -v `pwd`:/go/src/github.com/measurement-kit/go-measurement-kit \
  openobservatory/mk-alpine:20190509
```

Once in the container, do:

```bash
export GOPATH=/go
apk add go
cd /go/src/github.com/measurement-kit/go-measurement-kit
```

Then you're all set. Just `go get -v ./...` as usual.

### MinGW

Run `./download-libs.sh` to download the prebuilt libraries for all platforms.

You can also specify just a single plaform with:

```
./download-libs.sh mingw
```

Supported platforms are: `mingw`


## Examples

See the `_examples/` directory.

## Windows

You can cross compile from macOS. To this end, please install the
mingw-w64-cxx11 toolchain formula from our [homebrew tap](
https://github.com/measurement-kit/homebrew-measurement-kit).

Once you have such toolchain, you should be able to get going by
running the following commands:

```
CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 CGO_ENABLED=1 go build -x .

CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 CGO_ENABLED=1 go build -x _examples/ndt/ndt.go
wine ndt.exe

CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 CGO_ENABLED=1 go build -x _examples/web_connectivity/web_connectivity.go
wine web_connectivity.exe
```

It is anyway recommended to _also_ test using a real Windows system.
