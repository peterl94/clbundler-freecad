from clbundler.formula import *
        
class python(Formula):
    version = "2.7.8"
    source = {
        "type":"archive", 
        "url":"https://www.python.org/ftp/python/{0}/Python-{0}.tar.xz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(python, self).__init__(context, options)
        
        self.add_deps("openssl", "sqlite3", "tk")
        
        self.patches = ["pyconfig"]
        if vc_version(context.toolchain) > 9:
            self.patches.append("vc12_upgrade")
        else:
            self.patches.extend(["eha_option", "vcproj_bundle_libs"])
        
    def build(self):
        self.context.env["BUNDLE_PATH"] = self.context.bundle_path
        
        os.chdir("PCbuild")
        
        vc_ver = "v{0}0".format(vc_version(self.context.toolchain))
        
        #ignore errors because we don't need the modules that fail to build
        if "debug" in self.variant:
            vcbuild(self.context, "pcbuild.sln", "Debug",
                    extra=["/p:PlatformToolset=" + vc_ver], ignore_errors=True)
        if "release" in self.variant:
            vcbuild(self.context, "pcbuild.sln", "Release",
                    extra=["/p:PlatformToolset=" + vc_ver], ignore_errors=True)
        
        os.chdir("..")
        
        files = FileSet()
        files.add(["Include/*"], "include/python2.7", category=Categories.build)
        files.add(["Lib/*"], "bin/Lib", category=Categories.run)
        files.add(["PC/pyconfig.h"], "include/python2.7", category=Categories.build)
        
        os.chdir("PCbuild")
        if self.context.arch == "x64":
            os.chdir("amd64")
        
        files.add(["python27.lib", "python27_d.lib"], "lib", category=Categories.build)
        files.add(["python.exe", "*[!d].dll"], "bin", category=Categories.run)
        files.add(["*[!d].pyd"], "bin/DLLs", category=Categories.run)
        files.add(["python_d.exe", "*_d.dll", "python27_d.pdb"], "bin", category=Categories.run_dbg)
        files.add(["*_d.pyd"], "bin/DLLs", category=Categories.run_dbg)
        
        return files
