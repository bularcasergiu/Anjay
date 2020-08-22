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


    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="/home/sebu/workspace/Anjay", build_folder="/home/sebu/workspace/Anjay")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="/home/sebu/workspace/Anjay/include_public")
        self.copy("*.so*", dst="lib", src="/home/sebu/workspace/Anjay/output/lib")
        self.copy("*.cmake", dst="cmake", src="/home/sebu/workspace/Anjay/output/cmake")
        self.copy("*", dst="bin", src="/home/sebu/workspace/Anjay/output/bin")

    def package_info(self):
        self.cpp_info.libs = ["anjay"]

