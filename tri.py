# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import slic
from skimage.measure import regionprops
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.image as mpimg
import matplotlib.delaunay as triang
import sys

if len(sys.argv) == 1:
    print 'uso: ./%s <arquivo PNG>' % sys.argv[0]
    sys.exit()

IMG = sys.argv[1]

fig, ax3 = plt.subplots(ncols=1, figsize=(18, 18))

# abrimos a imagem
image_rgb = mpimg.imread(IMG)

# segmentamos em regiões
labels = slic(image_rgb,
              convert2lab=True,
              ratio=-10,
              n_segments=100,
              sigma=.1,
              max_iter=10)
conexos = labels

ax3.imshow(np.ones(image_rgb.shape))

# calculamos os boundingbox e centróides das regiões
# guardamos os pontos dos boundingbox em 'pontos'
pontos = []
for region in regionprops(conexos, ['Area', 'BoundingBox', 'Centroid']):
    minr, minc, maxr, maxc = region['BoundingBox']
    x0 = region['Centroid'][1]
    y0 = region['Centroid'][0]

    pontos.append([minc, minr])
    pontos.append([maxc, minr])
    pontos.append([minc, maxr])
    pontos.append([maxc, maxr])

pontos = np.array(pontos)

# calculamos pontos dos triânbulos através de Delaunay
cens, edg, tri, neig = triang.delaunay(pontos[:,0], pontos[:,1])
patches = []
cores = []
coords_tri = []
for t in tri:
  # t[0], t[1], t[2] are the points indexes of the triangle
  t_i = [t[0], t[1], t[2], t[0]]
  t_i2 = [t[0], t[1], t[2]]
  coords_tri.append([list(aa) for aa in list(pontos[:,[0,1]][t_i2])])
  x = pontos[:,0][t_i][0]
  y = pontos[:,1][t_i][0]

  # a cor do polígono vem da imagem original            
  cores.append(image_rgb[y-1][x-1])
    
  # criamos um polígono para representar o triângulo (aqui começa o desenho
  # que estamos sintetizando)
  poly = Polygon(pontos[:,[0,1]][t_i], True)
  patches.append(poly)

# adicionamos os polígonos a uma coleção de colagens
p = PatchCollection(patches)

# definimos as cores conforme imagem original  e as bordas em transparente
p.set_facecolor(cores)
p.set_edgecolor(cores)

# plotamos o desenho sintetizado
ax3.add_collection(p)

ax3.axis('off')
nome_pintura = '%s_pintura.svg' % IMG[:-4]
fig.savefig(nome_pintura)

print 'pintura gerada em: %s' % nome_pintura 

# lista com coordenadas de cada triângulo
# print 'coords. triângulos:', coords_tri
# número de triângulos
# print 'num. de triângulos:', len(coords_tri)
