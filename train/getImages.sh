#!/usr/bin/env bash

mkdir empty_background/
wget -r -np -nH --cut-dirs=3 http://euca-169-231-235-166.eucalyptus.cloud.aristotle.ucsb.edu/empty/ -P empty_background/
rm -rf empty_background/index*