# BOX 2: AUTOMATED CONTENT DETECTION FROM SOCIAL MEDIA IMAGES

Supplementary information for Box 2 in *Toivonen, T., Heikinheimo, V., Fink, C., Hausmann, A., Hiippala, T., Järv, O., Tenkanen, H., Di Minin, E. (2019). Social media data for conservation science: a methodological overview. Biological Conservation.*

## Dense captioning

For dense captioning, we used the DenseCap model [as implemented by the authors](https://github.com/jcjohnson/densecap) in Torch. To set up the framework and the model, follow the instructions provided by the authors.

DenseCap provides the output in JSON format. Because the default visualization is occasionally difficult to interpret, we provide an additional script for this purpose.

The visualization script requires numpy and matplotlib. You can install them using the command `pip install matplotlib numpy`.

To visualize DenseCap output, use the `viz_densecap.py` Python script in this directory. Running the script requires three parameters, which are (1) path to the directory with images (-i/--images), (2) path to the JSON file containing DenseCap output (-j/--json) and (3) the number of bounding boxes to draw (-b/--boxes).

To exemplify, execute the command `python viz_densecap.py -i imgs/ -j densecap.json -b 5` to draw five bounding boxes for each image in the output file `densecap.json`, whose images are stored in directory `imgs`.


## Instance segmentation

For instance segmentation, we used the [Detectron](https://github.com/facebookresearch/Detectron) platform developed by Facebook AI Research (FAIR).

The model used to create the examples presented in the article, Mask R-CNN, is available through the Detectron platform.

For up-to-date instructions on how to install the platform and required models, please see the Detectron repository.