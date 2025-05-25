version_strings = [
    # Standard Semantic Versioning
    "1.0.0",
    "2.1.3",
    "0.9.8",
    "1.2.3",
    "1.0.0-alpha",
    "1.0.0-alpha.1",
    "1.0.0-beta",
    "1.0.0-beta.2",
    "1.0.0-rc.1",
    "1.0.0+build.1",
    "1.0.0-alpha+build.1",
    "1.2.3-pre",
    "1.2.3-pre+meta",
    "1.2.3+meta",
    "1.2.3-beta+exp.sha.5114f85",
    "1.0.0-0.3.7",
    "1.0.0-x.7.z.92",
    "1.0.0-alpha.beta",
    "1.0.0-alpha.beta.1+build.1.2",
    "1.0.0-x-y-z.–",

    # Invalid or problematic SemVer edge cases
    "1.0.0--",       # double hyphen
    "1.0.0-",        # trailing hyphen
    "1.0.0-01",      # numeric with leading zero

    # Calendar Versioning (CalVer)
    "2021.04.01",
    "2021.04",
    "20210401",
    "21.4.1",
    "2021.04.01.1",
    "2021.04.01-beta",
    "2021.04.01+build.1",
    "2021.04.01-alpha+build.1",
    "2021.04.01-rc.1",
    "2021.04.01-0.3.7",

    # Prefixes and identifiers
    "v1.0.0",
    "v2.0",
    "version1.0",
    "release-1.0",
    "1.0.0-final",
    "1.0.0release",
    "1.0.0_release",
    "1.0.0release1",

    # Extra components
    "1.0.0.0",
    "1.0",
    "1",
    "1.0.0.0.0.0.0.0",  # long version chain

    # Progressive simple versions
    "2",
    "3",
    "4",
    "5",
    "10",

    # Alphanumeric and complex versions
    "1.0.0a",
    "1.0.0b",
    "1.0.0c",
    "1.0.0rc1",
    "1.0.0dev",
    "1.0.0post1",
    "1.0.0-pre-alpha",
    "1.0.0_post_release",
    "1.0.0.snapshot",
    "1.0.0.preview",
    "1.0.0test",

    # Mixed casing and separators
    "1_0_0",
    "1-0-0",
    "1~0~0",
    "1.0.0.RELEASE",
    "1.0.0.Final",
    "1.0.0.GA",
    "1.0.0.CR1",
    "1.0.0.M1",

    # Pythonic/PyPI styles
    "1.0.dev456",
    "1.0a1",
    "1.0b2",
    "1.0rc3",
    "1.0.post456",
    "1.0-1",         # Debian style
    "1.0+abc.5",     # local version segment
    "1.0+ubuntu1",
    "1.0-ubuntu2",
    "1.0~beta1",
    "1.0.0b6.dev0",

    # Go/Java-like styles
    "v1",
    "v1.2",
    "v1.2.3",
    "v1.2.3-pre",
    "v2023.05.04",
    "v2023.05.04-beta",

    # Misc edge cases
    "1.0.0 (stable)",
    "1.0.0 [LTS]",
    "2021-04-01",    # ISO date format
    "vNext",
    "latest",
    "dev",
    "master",
    "main",
    "snapshot",
    "trunk",
    "edge",
    "beta",
    "nightly",
    "canary",
]
