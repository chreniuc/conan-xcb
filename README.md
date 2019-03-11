[Conan.io](https://conan.io) package recipe for [*xcb*](https://xcb.freedesktop.org/).

The libxcb package provides an interface to the X Window System protocol, which replaces the current Xlib interface. Xlib can also use XCB as a transport layer, allowing software to make requests and receive responses with both. 

## For Users: Use this package

### Basic setup

    $ conan install xcb/1.13.1@chreniuc/test

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    xcb/1.13.1@chreniuc/test

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.


## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create chreniuc/test


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| shared      | False |  [True, False] |
| fPIC      | True |  [True, False] |

## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package cairo.
It does *not* in any way apply or is related to the actual software being packaged.

## TODO

 - test_package