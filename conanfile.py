from conans import ConanFile, CMake, tools


class SebuConan(ConanFile):
    name = "anjay"
    version = "1.0.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Hello here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    generators = "cmake"
    exports_sources = "*", ".git"
    no_copy_source=True

    def source(self):
        self.run("cmake . -DDTLS_BACKEND=""")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_folder, build_folder=self.source_folder)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="include_public")
        self.copy("*.so*", dst="lib", src="output/lib")
        self.copy("*.cmake", dst="cmake", src="output/cmake")
        self.copy("*", dst="bin", src="output/bin")

    def package_info(self):
        self.cpp_info.libs = ["anjay"]

