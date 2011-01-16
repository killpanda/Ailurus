import apt

class DEidentify():
    def __getDesktopEnvironment(self,name):
        all_deps = []
        dic = {'kde' : 0, 'gnome' : 0}
        if not self.cache.__contains__(name):
            return -1,'nosuchpack'
        else:
            sections = self.cache[name].section.split('/')
            if 'kde' in sections > 0:
                return 1,'kde'
            if 'gnome' in sections >0:
                return 1,'gnome'
            def find_in_dep(dep,name):
                for i in dep:
                    if i.find(name) >= 0:return True
                return False
            
            def get_all_dep(self,dep,all_deps):
                for i in dep:
                    or_dep = i.or_dependencies
                    for o in or_dep:
                        if o.name in all_deps:
                            continue
                        else:
                            all_deps += [o.name]
                            if self.cache.__contains__(o.name):
                                get_all_dep(self,self.cache[o.name].candidateDependencies,all_deps)
          
            dep = self.cache[name].candidateDependencies
            get_all_dep(self,dep,all_deps)
            if find_in_dep(all_deps, 'kde'):dic['kde'] += 1
            if find_in_dep(all_deps, 'gconf') or find_in_dep(all_deps, 'gnome'):dic['gnome'] += 1
            if dic['kde'] and not dic['gnome']:return 1,'kde'
            elif dic['gnome'] and not dic['kde']:return 1,'gnome'
            else:
                if 'universe' in sections or 'multiverse' in sections : 
                    return 1,'universe'
                else:
                    return 0,'notsure'
                    
    def getDE(self,names):
        namelist = names.split()
        ret = []
        for name in namelist:
            i,v = self.__getDesktopEnvironment(name)
            ret += [v]
            
        if 'nosuchpack' in ret:return 'nosuchpack'
        if 'kde' in ret and not 'gnome' in ret:return 'kde'
        if 'gnome' in ret and not 'kde' in ret:return 'gnome'

        return 'universe'
    
    def __init__(self):
        self.cache = apt.Cache()
        
    def reloadCache(self):
        self.cache = apt.Cache()

