from conans import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout

class libcmaesConan(ConanFile):
    name = "libcmaes"
    homepage = "https://github.com/CMA-ES/libcmaes"
    url = "https://github.com/CMA-ES/libcmaes"
    description = "libcmaes is a multithreaded C++11 library with Python bindings for high performance blackbox stochastic optimization using the CMA-ES algorithm for Covariance Matrix Adaptation Evolution Strategy"
    license = "MIT"

    def set_version(self):
        self.version = "0.10"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
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
    #exports_sources = ["../*"]
    def export_sources(self):
        self.output.info("Executing export_sources() method")
        self.copy("*", src="../src", dst="src")
        self.copy("CMakeLists.txt", src="../")
        self.copy("*", src="../include", dst="include")
        self.copy("*", src="../cmake", dst="cmake")
        self.copy("libcmaesConfig.cmake.in", src="../")
        self.copy("libcmaes.pc.in", src="../")

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
        cmake.configure()
        return cmake
        

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "libcmaes")
        self.cpp_info.set_property("cmake_target_name", "libcmaes::cmaes")
        self.cpp_info.set_property("pkg_config_name", "libcmaes")
