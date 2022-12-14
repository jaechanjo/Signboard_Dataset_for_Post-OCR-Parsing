Official Python Implementation

This work by JeongSoo Kim, HyungYoun Na, [Jaechan Jo](mailto:jjc12223a@gmail.com), Jaeseung Won, Wonil Lee, Sungwon Woo 
| [Paper](https://drive.google.com/file/d/1jmo093uR70ruJZR71bGKPc-naaCTbvY_/view?usp=share_link)

Multi Media System Lab, Sogang AI Research.

# Signboard_Dataset_for_Post-OCR_Parsing
We introduce a design of training dataset structure for extracting various information from shop sign for deep learning and parsing

![sample_image](https://user-images.githubusercontent.com/110301841/207096930-2a03162a-7177-47a8-85a0-991780c6cc18.jpg)


### Abstract
Recently, the demand for multimedia content has increased rapidly, and accordingly, plans for using multimedia content in various fields are being studied. It also includes roadview or road map data, which can help you quickly find out the status of stores by acquiring data from various shopping malls along with the recent surge in delivery services caused by the COVID-19 crisis. However, even if you want to obtain meaningful shopping mall information from the load view data using the Scene Text Recognition (STR) model, it is not suitable to extract only shopping mall information because the existing STR data is tagged to all characters in the Scene. Therefore, we propose a dataset with a new structure that is layered with signage objects – store names, phone numbers, and other unnecessary information for a dataset that handles only commercial information.




### Keyword(s)
Shop Sign Dataset, Post-OCR, Scene Text Detection, NER Task


### Class Definition
| Semantic Label |              |              | Description                                                                                              | 
| -------------- | ------------ | ------------ |  -----------------------------------------------------------------------   |
| meta           | version      |              | dataset version                                                                                          | 
|                | image_id     |              | corresponding image id                                                                                   | 
|                | image_path   |              | file path where the image is saved                                                                       | 
|                | image_height |              | height of image (by pixel)                                                                               | 
|                | image_width  |              | width of image (by pixel)                                                                                |
| -------------- | ------------ | ------------ |  -----------------------------------------------------------------------   | 
| roi            | points       |              | Four coordinates of quadrilateral                                                                        | 
|                | words        | is_vertical  | for a specific words, vertical shape shop sign                                                           |
|                |              | is_occlusion | for a specific words, part of the shop sign is covered by other objects such as tree, electric wire, etc |
|                |              | category     | store_name, telephone, noise, 3 types of words                                                           |
|                |              | text         | for a specific words, letters on the signboard                                                           |
|                | roi_name     |              | for a signboard, letters on the signboard                                                                | 
|                | occlusion    |              | for a signboard, part of the shop sign is covered by other objects such as tree, electric wire, etc      | 
|                | vertical     |              | for a signboard, vertical shape shop sign                                                                |


### Download link
| Category     | Total        | Link                                                                                  | Release Date |
| ------------ | ------------ | --------------------------------------------------                                    | ------------ |
| `Image`      | 1000         | https://drive.google.com/file/d/1s3zg9ltTTveDYGCUWkn3s2o1BSqnd-0i/view?usp=share_link | 13 Dec 2022  |
| `Label`      | 1000         | https://drive.google.com/file/d/1u0E5DlhL7dJlpfJBAtYLkt9cOjW3k414/view?usp=share_link | 13 Dec 2022  |



