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

fig, axes = plt.subplots(ncols=5, figsize=(18, 18))
ax0, ax1, ax2, ax3, ax4 = axes

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
for ax in axes:
    ax.clear()

ax0.imshow(image_rgb, cmap=plt.cm.gray, interpolation='nearest')
ax1.imshow(conexos, cmap=plt.cm.jet, interpolation='nearest')
ax2.imshow(conexos, cmap=plt.cm.jet, interpolation='nearest')
ax3.imshow(image_rgb, cmap=plt.cm.gray, interpolation='nearest')
ax4.imshow(np.zeros(image_rgb.shape))
ax0.set_title(u'Imagem original', fontsize=10)
ax1.set_title(u'Segmentação', fontsize=10)
ax2.set_title(u'Triangulação (Delaunay)', fontsize=10)
ax3.set_title(u'Imagem gerada', fontsize=10)
ax4.set_title(u'Apenas triângulos', fontsize=10)

# calculamos os boundingbox e centróides das regiões
# guardamos os pontos dos boundingbox em 'pontos'
pontos = []
for region in regionprops(conexos, ['Area', 'BoundingBox', 'Centroid']):
    minr, minc, maxr, maxc = region['BoundingBox']
    # plota boundingbox
    # rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
    #                           fill=False, edgecolor='red', linewidth=2)
    # ax1.add_patch(rect)
    x0 = region['Centroid'][1]
    y0 = region['Centroid'][0]
    # pontos.append([x0, y0])
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
  ax2.plot(pontos[:,0][t_i], pontos[:,1][t_i], 'k-', linewidth=.5)
  ax4.plot(pontos[:,0][t_i], pontos[:,1][t_i], 'w-', linewidth=.3)
  ax4.plot(pontos[:,0][t_i], pontos[:,1][t_i], 'wo', markersize=2)
  #print '---'
  t_i2 = [t[0], t[1], t[2]]
  #print pontos[:,[0,1]][t_i2]
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
#print 'patches:', len(patches), 'regions:', len(cores)
# definimos as cores conforme imagem original  e as bordas em transparente
p.set_facecolor(cores)
p.set_edgecolor(cores)
p.set_alpha(.8)
# plotamos o desenho sintetizado
ax3.add_collection(p)
for ax in axes:
  ax.axis('off')

nome_pintura = '%s_passos.svg' % IMG[:-4]
fig.savefig(nome_pintura)

print 'pintura gerada em: %s' % nome_pintura 

# lista com coordenadas de cada triângulo
# print 'coords. triângulos:', coords_tri
# número de triângulos
# print 'num. de triângulos:', len(coords_tri)
