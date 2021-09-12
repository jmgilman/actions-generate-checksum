# actions-generate-checksum

> Github action for generating checksum files

<a href="https://github.com/jmgilman/actions-generate-checksum/actions/workflows/ci.yml">
    <img src="https://github.com/jmgilman/actions-generate-checksum/actions/workflows/ci.yml/badge.svg"/>
</a>

This is a simple Github Action that calculates the checksum of files and outputs
the result into a local file. It's intended to be used in a release workflow
when there is a desire to include a checksum file with the release artifacts.

## Usage

The below example downloads release artifacts and generates checksums for the
zip and tar archives before creating a new release.

```yaml
jobs:
  release:
    name: Create release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout sources
        uses: actions/checkout@v2
      - name: Download releaseartifacts
        uses: actions/download-artifact@v2
        with:
          name: release-artifacts
          path: release
      - name: Generate checksum
        uses: jmgilman/actions-generate-checksum@v1
        with:
          patterns: |
            release/*.zip
            release/*.tar.gz
      - name: Create release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            checksum.txt
            release/*.zip
            release/*.tar.gz
```

## Options

The following options can be configured:

| Key        | Required | Default      | Description |
| ---------- | -------- | ------------ | ---------------------------------------------------- |
| `method`   | Optional | sha256       | Hashing algorithm to use [md5, sha1, sha256, sha512] |
| `output`   | Optional | checksum.txt | Output file path                                     | 
| `patterns` | Required | N/A          | List of glob patterns to use for matching files      | 