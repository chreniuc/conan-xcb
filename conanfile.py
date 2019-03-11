#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import glob
import shutil


class XCBConan(ConanFile):
    name = "xcb"
    version = "1.13.1"
    description = """The X protocol C-language Binding (XCB) is a replacement
        for Xlib featuring a small footprint, latency hiding, direct access to
        the protocol, improved threading support, and extensibility.s"""
    url = "https://github.com/chreniuc/conan-xcb"
    homepage = "https://xcb.freedesktop.org/"
    author = "Hreniuc Cristian-Alexandru <cristi@hreniuc.pw>"
    license = "GPL-3.0"
    exports = ["LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    source_subfolder = 'libxcb-%s' % version

    def source(self):
        archive_name = '%s.tar.gz' % self.source_subfolder
        # https://xcb.freedesktop.org/dist/libxcb-1.13.1.tar.gz
        tools.get('https://xcb.freedesktop.org/dist/%s' % archive_name)

    def build_requirements(self):
        self.build_requires('xcb-proto/1.13@chreniuc/test')

    def copy_pkg_config(self, name):
        root = self.deps_cpp_info[name].rootpath
        pc_dir = os.path.join(root, 'lib', 'pkgconfig')
        pc_files = glob.glob('%s/*.pc' % pc_dir)
        if not pc_files:  # zlib store .pc in root
            pc_files = glob.glob('%s/*.pc' % root)
        for pc_name in pc_files:
            new_pc = os.path.join('pkgconfig', os.path.basename(pc_name))
            self.output.warn('copy .pc file %s' % os.path.basename(pc_name))
            shutil.copy(pc_name, new_pc)
            prefix = root
            tools.replace_prefix_in_pc_file(new_pc, prefix)

    def build(self):
        with tools.chdir(self.source_subfolder):
            os.makedirs('pkgconfig')
            self.copy_pkg_config('xcb-proto')
            pkg_config_path = os.path.abspath('pkgconfig')
            # sed "s/pthread-stubs//" -i configure: This sed removes a
            # dependency on the libpthread-stubs package which is useless on Linux.
            # Source: http://www.linuxfromscratch.org/blfs/view/svn/x/libxcb.html
            self.run('sed -i "s/pthread-stubs//" configure')
            configure_args = ['--without-doxygen']
            if self.options.shared:
                configure_args.extend(['--disable-static', '--enable-shared'])
            else:
                configure_args.extend(['--enable-static', '--disable-shared'])

            env_build = AutoToolsBuildEnvironment(self)
            env_build.pic = self.options.fPIC
            env_build.configure(args=configure_args, pkg_config_paths=[pkg_config_path])
            env_build.make()
            env_build.install()

    def package(self):
        install = os.path.join(self.build_folder, "package")
        self.copy(pattern="*", dst="lib", src=os.path.join(install, "lib"))
        self.copy(pattern="*", dst="include", src=os.path.join(install, "include"))

    def package_info(self):
        self.cpp_info.libs = ['xcb', 'xcb-composite', 'xcb-damage', 'xcb-dpms', \
            'xcb-dri2', 'xcb-dri3', 'xcb-glx', 'xcb-present', 'xcb-randr', \
            'xcb-record', 'xcb-render', 'xcb-res', 'xcb-screensaver', \
            'xcb-shape', 'xcb-shm', 'xcb-sync', 'xcb-xf86dri', 'xcb-xfixes', \
            'xcb-xinerama', 'xcb-xinput', 'xcb-xkb', 'xcb-xtest', 'xcb-xv', \
            'xcb-xvmc']
        self.cpp_info.libs.extend(['Xau', 'Xdmcp']) # Dynamic, from system
