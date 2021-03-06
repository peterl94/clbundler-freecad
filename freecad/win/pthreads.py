from clbundler.formula import *
        
class pthreads(Formula):
    version = "2.9.1"
    source = {
        "type":"archive", 
        "url":"ftp://sourceware.org/pub/pthreads-win32/pthreads-w32-2-9-1-release.tar.gz"
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(pthreads, self).__init__(context, options)
        
    def build(self):
        if "debug" in self.variant:
            system.run_cmd("nmake", ["VC-debug"])
        if "release" in self.variant:
            system.run_cmd("nmake", ["VC"])
        
        files = FileSet()
        files.add(["pthread.h", "sched.h"], "include", category=Categories.build)
        files.add(["pthreadVC2.lib", "pthreadVC2d.lib"], "lib", category=Categories.build)
        files.add(["pthreadVC2.dll"], "bin", category=Categories.run)
        files.add(["pthreadVC2d.dll"], "bin", category=Categories.run_dbg)
        
        return files
        