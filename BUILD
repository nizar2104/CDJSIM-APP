android_binary(
    name = "android",
    manifest = "AndroidManifest.xml",
    deps = [":my_java_library"],
)

java_library(
    name = "my_java_library",
    srcs = glob(["*.java"]),
)

android_binary(
    name = "debug",
    manifest = "AndroidManifest.xml",
    deps = [":my_java_library"],
    debug = 1,
)
