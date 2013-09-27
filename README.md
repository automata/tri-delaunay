tri-delaunay
============

Generative paintings by Delaunay triangulation.

Presented at SIFISC 3 (2013) at IFSC/USP as:

    Pinturas generativas por tesselação de Delaunay. Estudo #4
    ----------------------------------------------------------

    Imagens de pinturas originais dos movimentos Barroco e Moderno foram
    segmentadas. Coordenadas de pontos pertencentes a esses segmentos foram dadas
    como entrada para o algoritmo de tesselação de Delaunay. O algoritmo cria uma
    malha a partir da triangulação das coordenadas dadas, sem cruzamentos de
    arestas. A cor de cada triângulo da malha equivale à cor média do segmento da
    pintura original.

# Installation

At a Linux workstation:

    sudo apt-get install python python-numpy python-matplotlib python-setuptools git
    git clone https://github.com/scikit-image/scikit-image.git
    cd scikit-image
    sudo python setup.py install
    cd ..
    
    git clone https://github.com/automata/tri-delaunay.git
    cd tri-delaunay

# Usage

To generate a painting from any PNG file:

    python tri.py foo.png
    
It will generate ''foo_pintura.svg''.
    
To generate a file showing all the steps:

    python tri_passos.py foo.png
    
It will generate ''foo_passos.svg''.

# Acknowledgements

LabMacambira.sf.net, IFSC/USP.
