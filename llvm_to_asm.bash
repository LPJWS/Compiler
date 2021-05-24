#!/bin/bash

llc -filetype=obj -relocation-model=pic output.ll
gcc output.o -o output