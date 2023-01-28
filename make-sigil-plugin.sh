#!/bin/sh

RELEASE=${1:-1.0.0}
DEST=lat2cyr
TMPDESTDIR=/tmp/${DEST}

mkdir ${TMPDESTDIR}
cp -r . ${TMPDESTDIR}
cd /tmp
rm -rf ${DEST}/.git* ${DEST}*.zip
sed -i -e "s/#VERSIONPLACEHOLDER#/${RELEASE}/g" ${DEST}/plugin.xml
zip ${DEST}.zip -r ${DEST} \
    -x ${DEST}/README.md -x ${DEST}/test_plugin.py -x ${DEST}/lib/__pycache__/ -x ${DEST}/lib/__pycache__/* \
    ${DEST}/LICENSE ${DEST}/*sh
unzip -t ${DEST}.zip
rm -rf ${TMPDESTDIR}
echo "Sigil plugin lat2cyr v${RELEASE} is ready in '/tmp/${DEST}.zip'"
