# [How to create custom COCO data set for object detection](https://www.dlology.com/blog/how-to-create-custom-coco-data-set-for-object-detection/) | DLology blog

## Quick start
1- Clone the repository.<br/>
2- run ```pip install -r requirements.txt```<br/>
3- Navigate to ```./data/coco/``` folder create `output.json` file.<br/>
4- Put your annotations in ```./data/VOC/Annotations``` folder.<br/>

5- Then you can run the `voc2coco.py` script to generate a COCO data formatted JSON file for you.
```
python voc2coco.py ./data/VOC/Annotations ./data/coco/output.json
```
Then you can run the following Jupyter notebook to visualize the coco annotations. `COCO_Image_Viewer.ipynb`


Further instruction on how to create your own datasets, read the [tutorial](https://www.dlology.com/blog/how-to-create-custom-coco-data-set-for-object-detection/).
