from conans import ConanFile, CMake, tools
from conans.tools import load
from conan.tools.cmake import CMakeToolchain
from conan.tools.layout import cmake_layout
import re, os, functools

required_conan_version = ">=1.43.0"

class libcmaesConan(ConanFile):
    name = "libcmaes"
    homepage = "https://github.com/CMA-ES/libcmaes"
    short_paths = True
    url = "https://github.com/CMA-ES/libcmaes"
    description = "libcmaes is a multithreaded C++11 library with Python bindings for high performance blackbox stochastic optimization using the CMA-ES algorithm for Covariance Matrix Adaptation Evolution Strategy"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"

    requires = "eigen/3.4.0"
    
    generators = "CMakeToolchain"
    #generators = "cmake"

    scm = {
        'type': 'git',
        'url': 'auto',
        'revision': 'auto',
        'verify_ssl': False
    }

    def set_version(self):
        content = load(os.path.join(self.recipe_folder, "CMakeLists.txt"))
        value=re.search(r"set\(libcmaes_VERSION (.*)\)", content)
        print(value)
        extracted_version  = value.group(1).strip()
        
        git = tools.Git(folder=self.recipe_folder)
        if (git.get_tag() != None):
            # depending on your workflow you could also
            # set a non-beta version when on main branch or
            # on a certain release branch
            self.version = extracted_version
        else:
            # if not tag -> pre-release version
            commit_hash = git.get_commit()[:8]
            branch_name = git.get_branch()[:9]
            self.version = f"{extracted_version}-{branch_name}.{commit_hash}"

    # Binary configuration
    options = {
        "shared": [True, False], 
        "openmp": [True, False],
        "surrog": [True, False]
        }
    default_options = {
        "shared": True, 
        "openmp": True,
        "surrog": True
        }

    # Sources are located in the same place as this recipe, copy them to the recipe
    def export_sources(self):
        pass
        #self.output.info("Executing export_sources() method")
        # self.copy("*", src="src", dst="src")
        # self.copy("CMakeLists.txt", src="../")
        # self.copy("*", src="include", dst="include")
        # self.copy("*", src="cmake", dst="cmake")
        # self.copy("libcmaesConfig.cmake.in", src=".")
        # self.copy("libcmaes.pc.in", src=".")

    def config_options(self):
        pass

    def configure(self):
        del self.settings.compiler.libcxx
        if not self.settings.get_safe("compiler.version"):
            del self.settings.compiler.version

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables['LIBCMAES_BUILD_EXAMPLES']=False
        tc.variables['LIBCMAES_BUILD_SHARED_LIBS'] = self.options.shared
        tc.variables['LIBCMAES_USE_OPENMP'] = self.options.openmp
        tc.variables['LIBCMAES_ENABLE_SURROG'] = self.options.surrog
        tc.generate()


    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['LIBCMAES_BUILD_EXAMPLES']=False
        cmake.definitions['LIBCMAES_BUILD_SHARED_LIBS']= self.options.shared
        cmake.definitions['LIBCMAES_USE_OPENMP']= self.options.openmp
        cmake.definitions['LIBCMAES_ENABLE_SURROG']= self.options.surrog
        cmake.configure()
        return cmake
        

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):        
        cmake = self.configure_cmake()
        #cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["libcmaes"]
