## Packaging Tools

These are tools that help preparing/operating/modifying patches and
`.spec` files during the tough life of packagers.

### Patch remixer

So you are a package maintainer. As a first step, you use the whole
[OBS](http://openbuildservice.org) because you do not want to live in
a stone age clinging rocks to get a fire. But as a next step, you
aren't happy to use [Quilt](http://savannah.nongnu.org/projects/quilt)
from back to 2003 (a bronze age, to be fair), so you want to
be modern and keep all your patches in the Git repository, instead of
directly inside your package.

But you quickly discover that Git has some limitations, which
are preventing you from
[getting it right](https://en.opensuse.org/openSUSE:Packaging_Patches_guidelines). Limitations
are these:

1. Naturally, Git creates patches with an order number:
   `NNNN_commit_name.patch`, so you know the order which patch after
   which. But the `NNNN` thing generates
   [all the problems for you](https://en.opensuse.org/openSUSE:Packaging_Patches_guidelines#Patch_naming). 

2. After you renamed patches, you now need to keep track of their
   order inside your `.spec` file. It might work with 10-20 patches,
   but you will get lost if they are exceeding 20 and you need to
   "shuffle" them around, shifting their order during version update
   etc.

3. In package terms, a commit to a Git is not always a patch. A patch
   may contain (and usually does) several commits. So every time you
   squash few commits into one patch and then rebase the whole
   thing, you usually do `force-push`. This is perfectly OK for
   tracking the patches in a dedicated Git repo. However `force-push`
   renders commit ID changing, while an _actual code_ mostly do not
   change. The package changelog and its history, however, reflects
   this change, because it is a valid diff. So your package reviewer
   might see countless "changes" that aren't as such.

The `git-format-pkg-patch` tool is here to:

1. Format patches from a specific range of commits or tags etc.
2. Re-format them the way they are compatible with OBS change tracking policies
3. Replace/update existing patches if necessary
4. Generate an inclusion text file for `.changes` log
5. Use those patches that actually makes sense to be replaced.

#### Man pages & docs

Please read [up to date man page](https://github.com/openSUSE/git-packaging-tools/blob/master/doc/git-format-pkg-patch.md).

#### Typical example

First, you create your patches somewhere within your Git project **foo**:

1. `mkdir -p /home/you/foo/patches`
2. `git-format-pkg-patch -f TAG`

Where `TAG` is your release tag (or commits range if you don't use
tagging) in Git against which you are creating your set of patches.

Second (version A), assuming `/home/you/foo/patches` is accessible, so
you go to your OBS project and update the patches with it:

1. `cd /home/you/obs/project`
2. `git-format-pkg-patch -u /home/you/foo/patches`

It will report you what was added/changed/removed and will generate a text file
`patches.changes.txt` in the same directory, which you can reuse to
include its content into `.changes` log of the package.

Second (version B), you do the same as above, except add option `-c`
during the next step like this:

`git-format-pkg-patch -u /home/you/foo/patches -c`

This will do the same as above, but will _actually_ update the
contents of those files.
