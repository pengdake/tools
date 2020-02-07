import os
import re
import commands

#local image file name pattern
IMG_PATTERN = re.compile(r'.*\.tar$')
#image tag pattern
TAG_PATTERN = re.compile(r"(\d)+\.(\d)+\.(\d)+-[cg]pu")
#image name prefix pattern
NAME_PATTERN = re.compile(r'(\w)+-base')
# local image path
PATH="/root/pdk"
# url about harbor project
HARBOR="10.1.0.50:30050/library"


for root, _, files in os.walk(PATH):
    for f in files:
        if IMG_PATTERN.match(f):
           img_path = os.path.join(root, f)
             
           s, o = commands.getstatusoutput("docker load -i %s" % img_path)
           if s:
              print("%s load failed!" % f)
           else:
              print("%s load successed!" % f)
           img_pre = NAME_PATTERN.search(f).group()
           img_tag = TAG_PATTERN.search(f).group()
           img_name = ':'.join([img_pre, img_tag])
           img_url = os.path.join(HARBOR, img_name)
           s, o = commands.getstatusoutput("docker tag %s %s" % (img_name, img_url))
           if s:
              print("%s tag failed!" % img_url)
           else:
              print("%s tag successed!" % img_url)
           s, o = commands.getstatusoutput("docker push %s" % img_url)
           if s:
              print("%s push failed!" % img_url)
           else:
              print("%s push successed!" % img_url)
           
        
            
