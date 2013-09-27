#!/bin/bash

for i in *.png; do autotrace "$i" -despeckle-level 14 --output-file "$(echo $i | sed 's/.png/.svg/')"; done