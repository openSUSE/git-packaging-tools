git-format-pkg-patch (1) -- Git to OBS patch remixer
====================================================

## SYNOPSIS

usage: git-format-pkg-patch [-h] [-u UPDATE] [-f FORMAT] [-o ORDERING]
                            [-x INDEX] [-s SPEC] [-i] [-c] [-e] [-v]


## DESCRIPTION

**git-format-pkg-patch** provides a high-level commandline interface
for the patch operations. It is intended as an end user
interface and enables some options better suited for interactive
usage by default compared to more specialized tools like
Emacs or bad ideas like Vim.

Package maintainer can use this utility
in order to:

1. Format patches from a specific range of commits or tags etc.
2. Re-format them the way they are compatible with OBS change tracking
policies
3. Replace/update existing patches if necessary
4. Generate an inclusion text file for `.changes` log.
5. Generate an inclusion text file for `.spec` file.

## OPTIONS

* `-u, --update`:
  Update current patches of the RPM package with the destination path
  where Git extracted patches are located.

* `-f, --format`:
  Specify tag or range of commits for patches to be formatted from the
  Git so they are compatible with the OBS package.

* `-o, --ordering`:
  Specify ordering spec inclusion file. Default: `patches.orders.txt`
  in the current directory where Git patches are also extracted to.

* `-x, --index`:
  Specify start ordering index for patches. Default: `0`.

* `-s, --spec`:
  Remix spec file and extract sources with their comments to match new
  patch ordering. This will replace new patches with new orders
  reusing already existing comments.

* `-i, --increment`:
  Use increments for unique names when patch commits repeated.

* `-c, --changed`:
  Update also changed files with the content.

* `-e, --existing`:
  Work with already formatted patches from Git, using `format-patches`
  command.

* `-v, --version`:
  Show current version and exit.

## EXAMPLES

### Create patches from Git

Extract patches from the Git, alredy formatted for the typical RPM
package:

- Create an _empty_ directory within the Git project, in which
patches are going to be created.

- Create patches against a tag `foo`, example:

```
$ git-format-patch -f foo
```

- In the file `patches.orders.txt` will be a reformatted list of
patches that needs to be included into the `.spec` file later.

- You can specify another ordering file name/location with an option
`-o` flag.

### Update OBS package (RPM) with extracted patches

- Assuming patches are alredy extracted (see an exmple above), change
to the root directory of the RPM package (an OBS project).

- **Option A**: Update the project with the set of patches (patches
that are with the same filenames but are changed at the code level
will be _only reported_ but will never be updated:

```
$ cd /to/obs/project
$ git-format-patch -u /path/to/your/patches
```

- **Option B**: Update the project with the set of patches including
patches that are with the same names but changed at the code level,
add flag `-c`:

```
$ cd /to/obs/project
$ git-format-patch -u /path/to/your/patches -c
```

### Remix spec file

The `git-format-patch` offers an helper functionality that allows to
remix the ordering file (where order of new patches is enlisted) with
the existing `.spec` file, extracting useful comments for each patch.

This funtion has a conventional limitations, as follows:

- Patch has to be commented above it, and have no empty
lines. Example:

```
# This comment is ignored, because there an empty line below

# This comment is accepted
# This comment is also accepted
Patch1:          filename-of-the.patch

# This is comment for foobar.patch below
Patch2:          foobar.patch
```

- Match of the patches are done by the _filename_, therefore it has to
be exact.

- In case there is no comment found, "Description N/A" is inserted.

That said in order to remix the ordering with the existing spec file,
do the following:

```
git-format-patch -s /path/to/project.spec \
                 -o /path/to/patches.orders.txt > result.txt
```

Although an actual patching directives are not processed and still
must be double-checked by the package maintainer.

## AUTHOR

  Bo Maryniuk <bo@suse.de>

## LINKS

For OBS guidelines:

* https://en.opensuse.org/openSUSE:Packaging_Patches_guidelines

For OBS general operations:

* http://en.opensuse.org/openSUSE:Build_Service_Tutorial
* http://en.opensuse.org/openSUSE:OSC

## SEE ALSO

osc(1), rpm(1), git-format-patch(1)
