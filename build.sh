#!/bin/bash

function get_version() {
    echo $(./git-format-pkg-patch -v | sed -e 's/.*: //g')
}


function get_archive_name() {
    echo "git-packaging-tools-$(get_version).tar.gz"
}


function cleanup() {
    if [ -d "$1" ]; then
	rm -rf $1
    fi
}

dirname="git-packaging-tools-$(get_version)"
cleanup $dirname
mkdir $dirname
cp git-format-pkg-patch $dirname
cp doc/*.1 $dirname
tar cvf - $dirname | gzip -9 > $(get_archive_name)
rm -rf $dirname
echo "Done"
