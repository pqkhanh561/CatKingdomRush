import re
import json



infos = dict()

with open("animation.txt", "r") as f:
  lines = f.readlines()
  for l in lines:
    try:
      info = re.search("createAnimation\(.*", l).group().replace("createAnimation(\"", '').replace(");", '').replace("\"", '').split("),")
      info[0] = info[0].split(',')
      info[0][0] = info[0][0].replace(' ', '')
      info[1] = info[1].replace("\"", '').rsplit('_', 1)
      info[1][0] = info[1][0].replace(' ', '')
    except IndexError:
      continue 
    try:
      if info[1][0] not in infos:
        infos.update({
          info[1][0]: {
            info[1][1]: {
              "prefix": info[0][0],
              "start": int(info[0][1]),
              "end": int(info[0][2]),
              "delay": float(info[0][3].replace(' ', '').replace('f', ''))
            }
          }
        })
      else:
        infos[info[1][0]].update(
          {
            info[1][1]: {
              "prefix": info[0][0],
              "start": int(info[0][1]),
              "end": int(info[0][2]),
              "delay": float(info[0][3].replace(' ', '').replace('f', ''))
            }
          }
        )
    except IndexError:
      print(info)
      infos.update({
        info[1][0]: {
          "prefix": info[0][0],
          "start": int(info[0][1]),
          "end": int(info[0][2]),
          "delay": float(info[0][3].replace(' ', '').replace('f', ''))
        }
      })

with open("object_sprite.json", "w") as f:
  f.write(json.dumps(infos, indent=4))
