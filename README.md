## Packaging Tools

This are tools that helps preparing/operating/modifying patches and spec files during the tough life of packager.

### Patch formatter

The `git-format-pkg-patch` tool is here to:

1. Format patches from a specific range of commits or tags etc.
2. Re-format them the way they are compatible with OBS change tracking policies
3. Replace/update existing patches if necessary
4. Generate an inclusion text file for `.changes` log

#### Usage

Usage is simple. Specify what you want to do:

- Format patches from the Git (`-f`)
- Update current patches in the OBS package (`-u`)

When updating, you can add an option `-c` that will not just tell you which
patch has been chaned, but also refresh it for you.

```
usage: git-format-pkg-patch [-h] [-u UPDATE] [-f FORMAT] [-c]

Git patch formatter for RPM packages

optional arguments:
-h, --help            show this help message and exit
-u UPDATE, --update UPDATE
update current patches with the destination path
-f FORMAT, --format FORMAT
specify tag or range of commits for patches to be
formatted
-c, --changed         update also changed files with the content
```

#### Typical routine

First, you create your patches somewhere:

1. `mkdir /home/you/foo`
2. `git-format-pkg-patch -f TAG`

Where `TAG` is your tag in Git against which you are creating your set of patches.

Second (version A), you go to your OBS project and update the patches with it:

1. `cd /home/you/obs/project`
2. `git-format-pkg-patch -u /home/you/foo`

It will report you what was added/changed/removed and will generate a text file
`patches.changes.txt` in the same directory, which you can reuse to include its content
into `.changes` log of the package.

Second (version B), you do the same as above, except add option `-c` during the next step like this:

`git-format-pkg-patch -u /home/you/foo -c`

This will do the same as above, but will _actually_ update the contents of those files.

