'''
**********************************************************************************************************************
                                        Quickly Fit Skeleton
**********************************************************************************************************************
    FILE NAME
        tajQuicklyFitSkeleton.py
        
    AUTHOR
        Bruce Tajtelbom - brucetaj@gmail.com 
            
    DESCRIPTION
 
        
    INPUT
    

    OUTPUT
        N/A
        
       
**********************************************************************************************************************
    VERSIONS 
        11/04/2022        1.00    start script 
        
**********************************************************************************************************************
    POSSIBLES UPDATES                                                                                     
        - N/A
**********************************************************************************************************************
    MAYA ICON LAUNCHER

import sys
import maya.cmds as mc
path = 'K:/3D/Packages/scripts/projects/TheBeastMaker/QuicklyFitSkeleton'
if path not in sys.path: 
    sys.path.append(path)
import tajQuicklyFitSkeleton as tQFS
reload(tQFS)
tQFS.constraintSkeletonUI()
**********************************************************************************************************************
'''
import maya.cmds as mc
import pymel.core as pm
import pymel.core.datatypes as dt

import os, sys, math
import shutil
import maya.mel
import cProfile
import random
import json


sys.dont_write_bytecode = True



#############################################################################################
##################################       GLOBAL DICS       ##################################
#############################################################################################

UI = {}
DT = {}

DT['leg']={'plane':True, 
           'vtx':[64, 66, 67, 68, 78, 79, 80, 88, 89, 90],
           'mesh':'proxy_Msh',
           'A':[64, 88],
           'B':[67],
           'C':[79, 78, 90, 80],
           'skip':[False, False, False], 
           'joints':['Hip', 'Knee','Ankle'], 
           'jointsPos':[[64, 88], [67, 66, 89, 68],[79, 78, 90, 80]],
           'jointsProj':[False, True, False],
           'npoSkip':[False, False, False],
           'jointsSkip':[False, False, False],
           'jointOrient':{'Hip':['Knee', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)],
                          'Knee':['Ankle', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)]} }

DT['arm']={'plane':True, 
           'vtx':[71, 81, 82, 83, 84, 85, 240, 241, 242, 243],
           'mesh':'proxy_Msh',
           'A':[71, 85],
           'B':[84],
           'C':[240, 241, 242, 243], 
           'skip':[False, False, False],
           'joints':['Shoulder', 'Elbow','Wrist'], 
           'jointsPos':[[71, 85], [81, 82, 83, 84],[240, 241, 242, 243]],
           'jointsProj':[False, True, False],
           'npoSkip':[False, False, False],
           'jointsSkip':[False, False, False],
           'jointOrient':{'Shoulder':['Elbow', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)],
                          'Elbow':['Wrist', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]} }

DT['spine']={'plane':True, 
             'vtx':[31, 32, 33, 35, 36, 38, 41, 42, 43, 44, 61, 62, 192, 193, 210],
             'mesh':'proxy_Msh',
             'A':[31],
             'B':[35],
             'C':[61, 62],
             'skip':['x', 'x', 'x'], 
             'joints':['Root', 'Spine1','Chest', 'Neck', 'Head', 'HeadEnd'], 
             'jointsPos':[[32, 33, 210, 43], [33, 35, 44, 210], [35, 44], [36, 38, 41, 42], [192, 193], [61, 62] ],
             'jointsProj':[False, False, False, False, False, False],
             'npoSkip':['x', 'x', 'x', 'x', 'x', 'x'],
             'jointsSkip':['x', 'z', 'z', 'z', 'z', 'z'],
             'jointOrient':{} }

DT['scapula']={'plane':False, 
               'vtx':[214, 213, 201, 200],
               'mesh':'proxy_Msh',
               'A':[],
               'B':[],
               'C':[],
               'skip':[False, False, False], 
               'joints':['Scapula'], 
               'jointsPos':[[214, 213, 201, 200]],
               'jointsProj':[False],
               'npoSkip':[False],
               'jointsSkip':[False],
               'jointOrient':{} }

DT['ear']={'plane':True, 
           'vtx':[184, 185, 186, 187, 188, 189, 190, 191],
           'mesh':'proxy_Msh',
           'A':[185, 191, 189, 187],
           'B':[189, 187, 186, 188],
           'C':[190, 188, 186, 184], 
           'skip':[False, False, False],
           'joints':['ear0', 'ear1'], 
           'jointsPos':[[190, 184, 185, 191], [186, 188, 187, 189]],
           'jointsProj':[False, False],
           'npoSkip':[False, False],
           'jointsSkip':[False, False],
           'jointOrient':{'ear0':['ear1', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)] } }

DT['footPivot']=['FootSideInner', 'ToesEnd', 'FootSideOuter', 'Heel']

DT['bigtoe']={'plane':True, 
              'vtx':[129, 126, 125, 134, 131, 130, 132, 133],
              'mesh':'proxy_Msh',
              'A':[129, 126, 125, 134],
              'B':[126, 131, 133, 129],
              'C':[131, 130, 132, 133], 
              'skip':[False, False, False],
              'joints':['BigToe1', 'BigToe2','BigToe3'], 
              'jointsPos':[[129, 126, 125, 134], [129, 126, 125, 134, 131, 130, 132, 133],[131, 130, 132, 133]],
              'jointsProj':[False, True, False],
              'npoSkip':[False, False, False],
              'jointsSkip':[False, False, False],
              'jointOrient':{'BigToe1':['BigToe2', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)],
                             'BigToe2':['BigToe3', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)]} }

DT['middletoe']={'plane':True, 
                 'vtx':[129, 127, 128, 134, 136, 137, 138, 135],
                 'mesh':'proxy_Msh',
                 'A':[129, 127, 128, 134],
                 'B':[129, 127, 135, 136],
                 'C':[136, 137, 138, 135], 
                 'skip':[False, False, False],
                 'joints':['MiddleToe1', 'MiddleToe2','MiddleToe3'], 
                 'jointsPos':[[129, 127, 128, 134], [129, 127, 128, 134, 136, 137, 138, 135], [136, 137, 138, 135]],
                 'jointsProj':[False, True, False],
                 'npoSkip':[False, False, False],
                 'jointsSkip':[False, False, False],
                 'jointOrient':{'MiddleToe1':['MiddleToe2', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)],
                                'MiddleToe2':['MiddleToe3', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)]} }

DT['index']={'plane':True, 
             'vtx':[16, 17, 18, 19, 20, 21, 25, 26, 27, 28, 29, 30, 97, 139],
             'mesh':'proxy_Msh',
             'A':[97, 139],
             'B':[25],
             'C':[29, 30, 16, 17], 
             'skip':[False, False, False],
             'joints':['IndexFinger1', 'IndexFinger2','IndexFinger3', 'IndexFinger4'], 
             'jointsPos':[[97, 139], [21, 20, 25, 26],[19, 18, 27, 28], [16, 17, 30, 29]],
             'jointsProj':[False, True, True, False],
             'npoSkip':[False, False, False, False],
             'jointsSkip':[False, False, False, False],
             'jointOrient':{'IndexFinger1':['IndexFinger2', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                            'IndexFinger2':['IndexFinger3', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                            'IndexFinger3':['IndexFinger4', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)]} }


DT['middle']={'plane':True, 
              'vtx':[0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 98, 140],
              'mesh':'proxy_Msh',
              'A':[98, 140],
              'B':[10],
              'C':[0, 1, 14, 15], 
              'skip':[False, False, False],
              'joints':['MiddleFinger1', 'MiddleFinger2','MiddleFinger3', 'MiddleFinger4'], 
              'jointsPos':[[98, 140], [4, 5, 10, 11], [2, 3, 12, 13], [0, 1, 14, 15]],
              'jointsProj':[False, True, True, False],
              'npoSkip':[False, False, False, False],
              'jointsSkip':[False, False, False, False],
              'jointOrient':{'MiddleFinger1':['MiddleFinger2', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                             'MiddleFinger2':['MiddleFinger3', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                             'MiddleFinger3':['MiddleFinger4', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)]} }

DT['ring']={'plane':True, 
             'vtx':[99, 141, 215, 216, 217, 218, 219, 220, 222, 223, 224, 225, 226, 227],
             'mesh':'proxy_Msh',
             'A':[99, 141],
             'B':[222],
             'C':[215, 216, 226, 227], 
             'skip':[False, False, False],
             'joints':['RingFinger1', 'RingFinger2','RingFinger3', 'RingFinger4'], 
             'jointsPos':[[99, 141], [219, 220, 222, 223], [217, 218, 224, 225], [215, 216, 226, 227]],
             'jointsProj':[False, True, True, False],
             'npoSkip':[False, False, False, False],
             'jointsSkip':[False, False, False, False],
             'jointOrient':{'RingFinger1':['RingFinger2', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                            'RingFinger2':['RingFinger3', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                            'RingFinger3':['RingFinger4', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)]} }

DT['pinky']={'plane':True, 
             'vtx':[96, 143, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239],
             'mesh':'proxy_Msh',
             'A':[96, 143],
             'B':[234],
             'C':[228, 229, 238, 239], 
             'skip':[False, False, False],
             'joints':['PinkyFinger1', 'PinkyFinger2','PinkyFinger3', 'PinkyFinger4'], 
             'jointsPos':[[96, 143], [232, 233, 234, 235], [230, 231, 236, 237], [228, 229, 238, 239]],
             'jointsProj':[False, True, True, False],
             'npoSkip':[False, False, False, False],
             'jointsSkip':[False, False, False, False],
             'jointOrient':{'PinkyFinger1':['PinkyFinger2', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                            'PinkyFinger2':['PinkyFinger3', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                            'PinkyFinger3':['PinkyFinger4', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)]} }

DT['thumb']={'plane':True, 
             'vtx':[95, 103, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 242],
             'mesh':'proxy_Msh',
             'A':[95, 103, 242],
             'B':[106],
             'C':[107, 108, 109, 110], 
             'skip':[False, False, False],
             'joints':['ThumbFinger1', 'ThumbFinger2','ThumbFinger3', 'ThumbFinger4'], 
             'jointsPos':[[95, 103, 242], [95, 106, 111, 112], [113, 114, 115, 116], [107, 108, 109, 110]],
             'jointsProj':[False, True, True, False],
             'npoSkip':[False, False, False, False],
             'jointsSkip':[False, False, False, False],
             'jointOrient':{'ThumbFinger1':['ThumbFinger2', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                            'ThumbFinger2':['ThumbFinger3', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
                            'ThumbFinger3':['ThumbFinger4', (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)]} }

DT['metacarpe']={'plane':True, 
                 'vtx':[92, 93, 94, 105],
                 'mesh':'proxy_Msh',
                 'A':[94, 105],
                 'B':[92, 105],
                 'C':[92, 93],
                 'skip':[False, False, False], 
                 'joints':['IndexFingerP', 'MiddleFingerP', 'RingFingerP', 'PinkyFingerP'], 
                 'jointsPos':[[92, 93, 94, 105], [92, 93, 94, 105], [92, 93, 94, 105], [92, 93, 94, 105]],
                 'npoValue':[[0.8, 0.11, 0.02, 0.09], [0.6, 0.08, 0.04, 0.29], [0.33, 0.13, 0.00, 0.64], [0.18, 0.05, 0.09, 0.83]],
                 'jointsProj':[False, False, False, False],
                 'npoSkip':[False, False, False, False],
                 'jointsSkip':[False, False, False, False],
                 'prefixe':{'IndexFingerP':'index', 'MiddleFingerP':'middle', 'RingFingerP':'ring', 'PinkyFingerP':'pinky'},
                 'jointOrient':{'IndexFingerP':['IndexFinger1', (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0)],
                                'MiddleFingerP':['MiddleFinger1', (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0)],
                                'RingFingerP':['RingFinger1', (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0)],
                                'PinkyFingerP':['PinkyFinger1', (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0)]} }

DT['toes']={'plane':False, 
               'vtx':[125, 126, 127, 128, 129, 134],
               'mesh':'proxy_Msh',
               'A':[],
               'B':[],
               'C':[],
               'skip':[False, False, False], 
               'joints':['Toes'], 
               'jointsPos':[[125, 126, 127, 128, 129, 134]],
               'jointsProj':[False],
               'npoSkip':[False],
               'jointsSkip':[False],
               'jointOrient':{} }

DT['eyebrowin']={'plane':True, 
               'vtx':[149, 150, 153, 154],
               'mesh':'proxy_Msh',
               'A':[153, 154],
               'B':[154, 150],
               'C':[149, 150],
               'skip':[False, False, False], 
               'joints':['EyebrowIn'], 
               'jointsPos':[[149, 150]],
               'jointsProj':[False],
               'npoSkip':[False],
               'jointsSkip':[False],
               'jointOrient':{} }

#############################################################################################
##################################          PATHS          ##################################
#############################################################################################




#############################################################################################
##################################      BASE INTERFACE     ##################################
#############################################################################################


#############################################################################################
##################################    LOOPS FORMLAYOUT     ##################################
#############################################################################################

def formLayout(argLayout, argControl, argInfos =[('None'), ('Form', 0), ('Ctrl', 0, ''), ('Pos', 0, 50)]):
    global UI

    places = ['top', 'bottom', 'left', 'right']

    for info, place in zip(argInfos, places):
        if info[0] == 'None':
            argLayout.attachNone(argControl, place)
        elif info[0] == 'Form':
            argLayout.attachForm(argControl, place, info[1] )
        elif info[0] == 'Ctrl':
            argLayout.attachControl(argControl, place, info[1], info[2] )
        elif info[0] == 'Pos':
            argLayout.attachPosition(argControl, place, info[1], info[2] )

#############################################################################################
##################################        INTERFACE        ##################################
#############################################################################################

def constraintSkeletonUI():
    '''
    '''
    global UI, DT

    loadPlugins()

    if pm.window('tQFS_UI', exists=True):
        pm.deleteUI('tQFS_UI', window=True)

    UI['windowtQFS'] = pm.window( 'tQFS_UI', title='Constraint Skeleton', widthHeight=(150, 200), s=True )
    UI['foL0'] = pm.formLayout(numberOfDivisions = 100)

    UI['button_leg'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                         align='left', 
                                         image1='newLayerEmpty.png',
                                         marginWidth = 15, 
                                         label = 'leg',
                                         backgroundColor = [0.40, 0.40, 0.40],
                                         width=150,
                                         height = 30, 
                                         command='tQFS.createConstraint(argKey=\'leg\', argScale=2.0)', 
                                         parent = UI['foL0'])
    UI['button_arm'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                         align='left', 
                                         image1='newLayerEmpty.png',
                                         marginWidth = 15, 
                                         label = 'arm',
                                         backgroundColor = [0.40, 0.40, 0.40],
                                         width=150,
                                         height = 30, 
                                         command='tQFS.createConstraint(argKey=\'arm\', argScale=2.0)', 
                                         parent = UI['foL0'])
    UI['button_spine'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                           align='left', 
                                           image1='newLayerEmpty.png',
                                           marginWidth = 15, 
                                           label = 'spine',
                                           backgroundColor = [0.40, 0.40, 0.40],
                                           width=150,
                                           height = 30, 
                                           command='tQFS.createConstraint(argKey=\'spine\', argScale=2.0)', 
                                           parent = UI['foL0'])
    UI['button_scapula'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                             align='left', 
                                             image1='newLayerEmpty.png',
                                             marginWidth = 15, 
                                             label = 'scapula',
                                             backgroundColor = [0.40, 0.40, 0.40],
                                             width=150,
                                             height = 30, 
                                             command='tQFS.createConstraint(argKey=\'scapula\', argScale=2.0)', 
                                             parent = UI['foL0'])
    UI['button_ear'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                         align='left', 
                                         image1='newLayerEmpty.png',
                                         marginWidth = 15, 
                                         label = 'ear',
                                         backgroundColor = [0.40, 0.40, 0.40],
                                         width=150,
                                         height = 30, 
                                         command='tQFS.createConstraint(argKey=\'ear\', argScale=1.5)', 
                                         parent = UI['foL0'])
    UI['button_footPivot'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                               align='left', 
                                               image1='newLayerEmpty.png',
                                               marginWidth = 15, 
                                               label = 'footPivot',
                                               backgroundColor = [0.40, 0.40, 0.40],
                                               width=150,
                                               height = 30, 
                                               command='tQFS.createALone(argKey=\'footPivot\', argScale=2.0)', 
                                               parent = UI['foL0'])

    UI['button_bigtoe'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                            align='left', 
                                            image1='newLayerEmpty.png',
                                            marginWidth = 15, 
                                            label = 'bigtoe',
                                            backgroundColor = [0.40, 0.40, 0.40],
                                            width=150,
                                            height = 30, 
                                            command='tQFS.createConstraint(argKey=\'bigtoe\', argScale=2.0)', 
                                            parent = UI['foL0'])

    UI['button_middletoe'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                               align='left', 
                                               image1='newLayerEmpty.png',
                                               marginWidth = 15, 
                                               label = 'middletoe',
                                               backgroundColor = [0.40, 0.40, 0.40],
                                               width=150,
                                               height = 30, 
                                               command='tQFS.createConstraint(argKey=\'middletoe\', argScale=2.0)', 
                                               parent = UI['foL0'])

    UI['button_index'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                           align='left', 
                                           image1='newLayerEmpty.png',
                                           marginWidth = 15, 
                                           label = 'index',
                                           backgroundColor = [0.40, 0.40, 0.40],
                                           width=150,
                                           height = 30, 
                                           command='tQFS.createConstraint(argKey=\'index\', argScale=1.5)', 
                                           parent = UI['foL0'])

    UI['button_middle'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                            align='left', 
                                            image1='newLayerEmpty.png',
                                            marginWidth = 15, 
                                            label = 'middle',
                                            backgroundColor = [0.40, 0.40, 0.40],
                                            width=150,
                                            height = 30, 
                                            command='tQFS.createConstraint(argKey=\'middle\', argScale=1.5)', 
                                            parent = UI['foL0'])

    UI['button_ring'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                            align='left', 
                                            image1='newLayerEmpty.png',
                                            marginWidth = 15, 
                                            label = 'ring',
                                            backgroundColor = [0.40, 0.40, 0.40],
                                            width=150,
                                            height = 30, 
                                            command='tQFS.createConstraint(argKey=\'ring\', argScale=1.5)', 
                                            parent = UI['foL0'])

    UI['button_pinky'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                            align='left', 
                                            image1='newLayerEmpty.png',
                                            marginWidth = 15, 
                                            label = 'pinky',
                                            backgroundColor = [0.40, 0.40, 0.40],
                                            width=150,
                                            height = 30, 
                                            command='tQFS.createConstraint(argKey=\'pinky\', argScale=1.5)', 
                                            parent = UI['foL0'])

    UI['button_thumb'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                            align='left', 
                                            image1='newLayerEmpty.png',
                                            marginWidth = 15, 
                                            label = 'thumb',
                                            backgroundColor = [0.40, 0.40, 0.40],
                                            width=150,
                                            height = 30, 
                                            command='tQFS.createConstraint(argKey=\'thumb\', argScale=1.5)', 
                                            parent = UI['foL0'])
    UI['button_metacarpe'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                            align='left', 
                                            image1='newLayerEmpty.png',
                                            marginWidth = 15, 
                                            label = 'metacarpe',
                                            backgroundColor = [0.40, 0.40, 0.40],
                                            width=150,
                                            height = 30, 
                                            command='tQFS.createConstraint(argKey=\'metacarpe\', argScale=1.5)', 
                                            parent = UI['foL0'])

    UI['button_toes'] = pm.iconTextButton(style='iconAndTextHorizontal',
                                            align='left', 
                                            image1='newLayerEmpty.png',
                                            marginWidth = 15, 
                                            label = 'toes',
                                            backgroundColor = [0.40, 0.40, 0.40],
                                            width=150,
                                            height = 30, 
                                            command='tQFS.createConstraint(argKey=\'toes\', argScale=2.0)', 
                                            parent = UI['foL0'])

    formLayout(UI['foL0'], UI['button_leg'], argInfos=[('Form', 5), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_arm'], argInfos=[('Ctrl', 5, UI['button_leg']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_spine'], argInfos=[('Ctrl', 5, UI['button_arm']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_scapula'], argInfos=[('Ctrl', 5, UI['button_spine']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_ear'], argInfos=[('Ctrl', 5, UI['button_scapula']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_footPivot'], argInfos=[('Ctrl', 5, UI['button_ear']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_bigtoe'], argInfos=[('Ctrl', 5, UI['button_footPivot']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_middletoe'], argInfos=[('Ctrl', 5, UI['button_bigtoe']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_index'], argInfos=[('Ctrl', 5, UI['button_middletoe']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_middle'], argInfos=[('Ctrl', 5, UI['button_index']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_ring'], argInfos=[('Ctrl', 5, UI['button_middle']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_pinky'], argInfos=[('Ctrl', 5, UI['button_ring']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_thumb'], argInfos=[('Ctrl', 5, UI['button_pinky']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_metacarpe'], argInfos=[('Ctrl', 5, UI['button_thumb']), ('None'), ('Form', 5), ('Form', 5)])
    formLayout(UI['foL0'], UI['button_toes'], argInfos=[('Ctrl', 5, UI['button_metacarpe']), ('None'), ('Form', 5), ('Form', 5)])
    
    pm.showWindow( UI['windowtQFS'] )
    UI['windowtQFS'].setWidth(250)
    UI['windowtQFS'].setHeight(70)

#############################################################################################
##################################         PROCESS         ##################################
#############################################################################################

def createALone(argKey='', argScale=1.0):
    global UI, DT 

    if not mc.objExists('FitSkeleton_cst'): root_glb=mc.createNode('transform', name='FitSkeleton_cst')
    else: root_glb='FitSkeleton_cst'
    
    if not mc.objExists(argKey+'_cst_grp'): root_cst=mc.createNode('transform', name=argKey+'_cst_grp', parent='FitSkeleton_cst')
    else: root_cst=argKey+'_cst_grp'

    if not mc.objExists(argKey+'_trackers_grp'): trackers=mc.createNode('transform', name=argKey+'_trackers_grp', parent=root_cst)
    else: trackers=argKey+'_trackers_grp'

    jnts=DT[argKey]
    for jnt in jnts:
        pos=mc.xform(jnt, ws=True, query=True, t=True)
        npo=mc.createNode('transform', name=argKey+'_'+jnt+'_npo', parent=root_cst)
        mc.setAttr(npo+'.t', pos[0], pos[1], pos[2])

        pntCtrl=[(0.6, 0.0, -0.3), (0.6, 0.0, 0.3), (0.3, 0.0, 0.6), 
                 (-0.3, 0.0, 0.6), (-0.6, 0.0, 0.3), (-0.6, 0.0, -0.3), 
                 (-0.3, 0.0, -0.6), (0.3, 0.0, -0.6), (0.6, 0.0, -0.3)]
        s=2.0
        pntCtrl=[(v[0]*s, v[1]*s, v[2]*s) for v in pntCtrl]
        k=[k for k in range(len(pntCtrl))]
        exec('temp=mc.curve(degree=1, p='+str(pntCtrl)+', k='+str(k)+', name=\"dede\")')
        ctrlShape=mc.ls(mc.listRelatives(temp, shapes=True,  noIntermediate=True), type='nurbsCurve')[0]
        ctrl_new=mc.createNode('transform', name=argKey+'_'+jnt+'_Ctrl')
        ctrl_guide=mc.createNode('guideLineShape', name=argKey+'_'+jnt+'_guide', parent=ctrl_new)
        mc.connectAttr(ctrlShape+'.worldSpace[0]', ctrl_guide+'.create', force=True)
        mc.delete(temp)
        mc.parent(ctrl_new, npo)
        mc.setAttr(ctrl_new+'.t', 0.0, 0.0, 0.0)
        mc.setAttr(ctrl_new+'.r', 0.0, 0.0, 0.0)

        mc.pointConstraint(ctrl_new, jnt)

        mc.setAttr(ctrl_guide+'.xRay', True)
        mc.setAttr(ctrl_guide+'.color', 0.513, 0.442, 0.283)     


    UI['button_'+argKey].setEnable(False)


def createConstraint(argKey='', argScale=1.0):
    global UI, DT 

    if not mc.objExists('FitSkeleton_cst'): root_glb=mc.createNode('transform', name='FitSkeleton_cst')
    else: root_glb='FitSkeleton_cst'
    
    if not mc.objExists(argKey+'_cst_grp'): root_cst=mc.createNode('transform', name=argKey+'_cst_grp', parent='FitSkeleton_cst')
    else: root_cst=argKey+'_cst_grp'

    if not mc.objExists(argKey+'_trackers_grp'): trackers=mc.createNode('transform', name=argKey+'_trackers_grp', parent=root_cst)
    else: trackers=argKey+'_trackers_grp'
        

    build=createProximityPin(argIdx=DT[argKey]['vtx'], argMesh=DT[argKey]['mesh'], argName=argKey, argRoot=trackers)
    mc.refresh(force=True)

    if DT[argKey]['plane']:
        ctrl, ctrl_A, ctrl_B, ctrl_C, plane, planeShape = createPlaneConstraint(argPrefixe=argKey)
        
        nodes_proxy=['displayPlane', 'root', 'ctrl', 'lines', 'plane', 'grid', 'dimensions', 'scalePlane', 'shortest', 'longest']
        for n in nodes_proxy:
            mc.addAttr(root_cst, longName=n, proxy=ctrl+'.'+n)

        mc.setAttr(root_cst+'.root', 0)
        mc.setAttr(root_cst+'.ctrl', 0)
        mc.setAttr(root_cst+'.lines', 0)
        mc.setAttr(root_cst+'.plane', 1)
        mc.setAttr(root_cst+'.grid', 0)
        mc.setAttr(root_cst+'.shortest', 1.5)

        mc.parent(ctrl, plane, root_cst)

        letters=['A', 'B', 'C']
        ctrls=[ctrl_A, ctrl_B, ctrl_C]
        i=0
        for l, ct in zip(letters, ctrls): 
            trackers=[]
            for ids in DT[argKey][l]:
                trackers.append(build[ids]['output'])
            trackers.append(ct)
            if DT[argKey]['skip'][i]:
                mc.pointConstraint(trackers, skip=DT[argKey]['skip'][i])
            else:
                mc.pointConstraint(trackers)
            i+=1

    for i, jnt in enumerate(DT[argKey]['joints']):
                
        if DT[argKey]['jointsProj'][i]:
            proxy=mc.createNode('transform', name=argKey+'_'+jnt+'_proxy', parent=root_cst)
            
            if isinstance(DT[argKey]['jointsPos'][i], list):
                trackers=[]
                for ids in DT[argKey]['jointsPos'][i]:
                    trackers.append(build[ids]['output'])
                trackers.append(proxy)
                if DT[argKey]['npoSkip'][i]:
                    mc.pointConstraint(trackers, skip=DT[argKey]['jointsSkip'][i])
                else:
                    mc.pointConstraint(trackers)

            npo=mc.createNode('transform', name=argKey+'_'+jnt+'_npo', parent=root_cst)
            closest=mc.createNode('closestPointOnMesh', name=argKey+'_cPOM')
            mc.connectAttr(planeShape+'.worldMatrix[0]', closest+'.inputMatrix', force=True)
            mc.connectAttr(planeShape+'.worldMesh[0]', closest+'.inMesh', force=True)
            mc.connectAttr(proxy+'.translate', closest+'.inPosition', force=True)
            mc.connectAttr(closest+'.position', npo+'.translate', force=True)
            mc.connectAttr(plane+'.rotate', npo+'.rotate', force=True)
        else:
            npo=mc.createNode('transform', name=argKey+'_'+jnt+'_npo', parent=root_cst)
            
            if isinstance(DT[argKey]['jointsPos'][i], list):
                trackers=[]
                for ids in DT[argKey]['jointsPos'][i]:
                    trackers.append(build[ids]['output'])
                trackers.append(npo)
                if DT[argKey]['npoSkip'][i]:
                    cst=mc.pointConstraint(trackers, skip=DT[argKey]['npoSkip'][i])[0]
                else:
                    cst=mc.pointConstraint(trackers)[0]

                if 'npoValue' in DT[argKey].keys():
                    wght=mc.pointConstraint(cst, query=True, weightAliasList=True)
                    for w, v in zip(wght, DT[argKey]['npoValue'][i]):
                        mc.setAttr(cst+'.'+w, v)

            if DT[argKey]['plane']:
                mc.connectAttr(plane+'.rotate', npo+'.rotate', force=True)

        pntCtrl=[(0.6, 0.0, -0.3), (0.6, 0.0, 0.3), (0.3, 0.0, 0.6), 
             (-0.3, 0.0, 0.6), (-0.6, 0.0, 0.3), (-0.6, 0.0, -0.3), 
             (-0.3, 0.0, -0.6), (0.3, 0.0, -0.6), (0.6, 0.0, -0.3)]
        s=argScale
        pntCtrl=[(v[0]*s, v[1]*s, v[2]*s) for v in pntCtrl]
        k=[k for k in range(len(pntCtrl))]
        exec('temp=mc.curve(degree=1, p='+str(pntCtrl)+', k='+str(k)+', name=\"dede\")')
        ctrlShape=mc.ls(mc.listRelatives(temp, shapes=True,  noIntermediate=True), type='nurbsCurve')[0]
        ctrl_new=mc.createNode('transform', name=argKey+'_'+jnt+'_Ctrl')
        ctrl_guide=mc.createNode('guideLineShape', name=argKey+'_'+jnt+'_guide', parent=ctrl_new)
        mc.connectAttr(ctrlShape+'.worldSpace[0]', ctrl_guide+'.create', force=True)
        mc.delete(temp)
        mc.parent(ctrl_new, npo)
        mc.setAttr(ctrl_new+'.t', 0.0, 0.0, 0.0)
        mc.setAttr(ctrl_new+'.r', 0.0, 0.0, 0.0)
        if DT[argKey]['plane']:
            attrs=['ty', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
            for at in attrs:
                mc.setAttr(ctrl_new+'.'+at, lock=True, keyable=False, channelBox=False)

        mc.setAttr(ctrl_guide+'.xRay', True)
        mc.setAttr(ctrl_guide+'.color', 0.513, 0.442, 0.283)
        
        if DT[argKey]['jointsSkip'][i]:
            mc.pointConstraint(ctrl_new, jnt, skip=DT[argKey]['jointsSkip'][i])
        else:
            mc.pointConstraint(ctrl_new, jnt)

    if DT[argKey]['plane']:
        orient=DT[argKey]['jointOrient']
        for jnt in orient.keys():
            if 'prefixe' in DT[argKey].keys():
                ctrl=DT[argKey]['prefixe'][jnt]+'_'+orient[jnt][0]+'_Ctrl'
            else:
                ctrl=argKey+'_'+orient[jnt][0]+'_Ctrl'
            mc.aimConstraint(ctrl, jnt, aimVector=orient[jnt][1], 
                                        upVector=orient[jnt][2],  
                                        worldUpVector=orient[jnt][3], 
                                        worldUpObject=plane, 
                                        worldUpType='objectrotation', maintainOffset=False, )
            mc.setAttr(jnt+'.displayLocalAxis', 1)

    UI['button_'+argKey].setEnable(False)

        
#############################################################################################
##################################          UTILS          ##################################
#############################################################################################



def createProximityPin(argVertices=[], argName='', argIdx=[], argMesh='', argRoot=''):
    global UI, DT


    parent=''
    child=''
    orig=''
    name=''
    allOutput={}
    
    if argIdx:
        if not mc.objExists(argMesh):
            mc.warning('Give an real object !')
            return
    
        if mc.nodeType(argMesh)=='transform':
            parent=argMesh
        elif mc.nodeType(argMesh)=='mesh':
            parent=mc.listRelatives(argMesh, parent=True)[0]
        else:
            mc.warning('Give a mesh or transform !')
            return
        argVertices=[]
        for ids in argIdx:
            argVertices.append(argMesh+'.vtx['+str(ids)+']')
        
    elif argVertices:
        
        parent=argVertices[0].split('.')[0]
        if not mc.objExists(argMesh):
            mc.warning('Give an real object !')
            return

    if argName:
        name=str(argName)
    else:
        name=str(parent)

    allOutput['parent']=parent
    childs=mc.listRelatives(parent, children=True)
    for ch in childs:
        if mc.getAttr(ch+'.intermediateObject')==0:
            child=ch
            allOutput['child']=child

    origParent=mc.duplicate(child, name=name+'_fakeOrig')[0]
    mc.setAttr(origParent+'.v', 0)
    if mc.listRelatives(origParent, parent=True):
        mc.parent(origParent, world=True)
    for each in mc.listRelatives(origParent, children=True, fullPath=True):
        if mc.getAttr(each+'.intermediateObject'):
            mc.delete(each)
        else:
            ok=each
    orig=ok.split('|')[-1]
    allOutput['orig']=orig

    if argRoot:
        mc.parent(origParent, argRoot)

    
        
    proximityPin=mc.createNode('proximityPin', name=name+'_ProximityPIn')
    mc.connectAttr(orig+'.outMesh', proximityPin+'.originalGeometry', force=True)
    mc.connectAttr(child+'.worldMesh[0]', proximityPin+'.deformedGeometry', force=True)
    allOutput['proximityPin']=proximityPin
    
    for i, vtx in enumerate(argVertices):
        indice=int(vtx.split('[')[1].split(']')[0])
        allOutput[indice]={}
        
        position=mc.xform(vtx, ws=True, query=True, t=True)
        inPut=mc.createNode('transform', name=name+'_In_'+str(indice))
        mc.setAttr(inPut+'.t', position[0], position[1], position[2])
        output=mc.createNode('transform', name=name+'_Out_'+str(indice))        
           
        mc.connectAttr(inPut+'.matrix', proximityPin+'.inputMatrix['+str(i)+']', force=True)
        mc.connectAttr(proximityPin+'.outputMatrix['+str(i)+']', output+'.offsetParentMatrix')

        if argRoot:
            mc.parent(inPut, output, argRoot)
        
        allOutput[indice]['output']=output
        allOutput[indice]['input']=inPut
        allOutput[indice]['position']=position

    return allOutput


def createPlaneConstraint(argPrefixe=''):
    global UI, DT
    '''
    '''
    p = argPrefixe
    loadPlugins()
    while mc.objExists(p+'_plane'):
        dialog=pm.promptDialog(title='Name', text=p+'bis', message='Enter New Name:', button=['OK', 'Cancel'], defaultButton='OK', 
                               cancelButton='Cancel', dismissString=None)
        if dialog == 'OK':
            p=pm.promptDialog(query=True, text=True)
        else:
            return

    ###### create Plane
    ##############################################################################################
    plane=mc.polyCreateFacet( p=[(-1, 0, -1), (-1, 0, 1), (1, 0, 1), (1, 0, -1)] )
    mc.delete(plane[1])
    plane=mc.rename(plane[0], p+'_plane')
    planeShape=mc.listRelatives(plane, shapes=True,  noIntermediate=True)[0]
    planeShape=mc.rename(planeShape, p+'_plane_mesh')

    mc.setAttr(planeShape+'.overrideEnabled', 1)
    mc.setAttr(planeShape+'.overrideDisplayType', 2)

    ###### create Plane Shader
    ##############################################################################################
    planeShader=mc.shadingNode('surfaceShader', asShader=True, name=p+'_plane_Shd')
    planeShaderSG=mc.sets(planeShader, renderable=True, empty=True, name=p+'_plane_ShdSG')
    mc.connectAttr(planeShader+'.outColor', planeShaderSG+'.surfaceShader', force=True)
    mc.sets(planeShape, edit=True, forceElement=planeShaderSG)

    mc.setAttr(planeShader+'.outTransparency', 0.83, 0.83, 0.83, type='double3')

    ###### create Grid
    ##############################################################################################
    pntGrid=[(-1.0, 0.0, -1.0), (-1.0, 0.0, 1.0), (-0.8, 0.0, 1.0), (-0.8, 0.0, -1.0), 
             (-0.6, 0.0, -1.0), (-0.6, 0.0, 1.0), (-0.4, 0.0, 1.0), (-0.4, 0.0, -1.0), 
             (-0.2, 0.0, -1.0), (-0.2, 0.0, 1.0), (0.0, 0.0, 1.0), (0.0, 0.0, -1.0), 
             (0.2, 0.0, -1.0), (0.2, 0.0, 1.0), (0.4, 0.0, 1.0), (0.4, 0.0, -1.0), 
             (0.6, 0.0, -1.0), (0.6, 0.0, 1.0), (0.8, 0.0, 1.0), (0.8, 0.0, -1.0), 
             (1.0, 0.0, -1.0), (1.0, 0.0, 1.0), (-1.0, 0.0, 1.0), (-1.0, 0.0, 0.8), 
             (1.0, 0.0, 0.8), (1.0, 0.0, 0.6), (-1.0, 0.0, 0.6), (-1.0, 0.0, 0.4), 
             (1.0, 0.0, 0.4), (1.0, 0.0, 0.2), (-1.0, 0.0, 0.2), (-1.0, 0.0, 0.0), 
             (1.0, 0.0, 0.0), (1.0, 0.0, -0.2), (-1.0, 0.0, -0.2), (-1.0, 0.0, -0.4), 
             (1.0, 0.0, -0.4), (1.0, 0.0, -0.6), (-1.0, 0.0, -0.6), (-1.0, 0.0, -0.8), 
             (1.0, 0.0, -0.8), (1.0, 0.0, -1.0), (-1.0, 0.0, -1.0)]
    k=[i for i in range(len(pntGrid))]
    exec('temp=mc.curve(degree=1, p='+str(pntGrid)+', k='+str(k)+', name=\"dede\")')
    gridShape=mc.ls(mc.listRelatives(temp, shapes=True,  noIntermediate=True), type='nurbsCurve')[0]
    gridShape=mc.rename(gridShape, p+'_plane_grid')
    mc.parent(gridShape, plane, add=True, shape=True)
    mc.delete(temp)

    mc.setAttr(gridShape+'.overrideEnabled', 1)
    mc.setAttr(gridShape+'.overrideDisplayType', 1)

    ###### create rigid Constraint
    ##############################################################################################
    rCons=mc.createNode('rigidCons', name=p+'_plane_rCons', parent=plane)

    ###### create zero transform
    ##############################################################################################
    z=mc.createNode('transform', name=p+'_zero')

    ###### create ctrls
    ##############################################################################################
    ctrl=mc.createNode('transform', name=p+'_ctrl')
     
    ctrl_A=mc.createNode('transform', name=p+'_A_ctrl', parent=ctrl)
    ctrl_B=mc.createNode('transform', name=p+'_B_ctrl', parent=ctrl)
    ctrl_C=mc.createNode('transform', name=p+'_C_ctrl', parent=ctrl)
    mc.setAttr(ctrl_A+'.tx', -1.0)
    mc.setAttr(ctrl_B+'.tz', -1.0)
    mc.setAttr(ctrl_C+'.tx', 1.0)

    ctrl_A_loc=mc.createNode('locator', name=p+'_A_ctrl_loc', parent=ctrl_A)
    ctrl_B_loc=mc.createNode('locator', name=p+'_B_ctrl_loc', parent=ctrl_B)
    ctrl_C_loc=mc.createNode('locator', name=p+'_C_ctrl_loc', parent=ctrl_C)

    mc.setAttr(ctrl_A_loc+'.localScale', 0.0, 0.0, 0.0)
    mc.setAttr(ctrl_B_loc+'.localScale', 0.0, 0.0, 0.0)
    mc.setAttr(ctrl_C_loc+'.localScale', 0.0, 0.0, 0.0)

    mc.addAttr(ctrl, cachedInternally=True, shortName='displayPlane', longName='displayPlane', 
               niceName='____________________', enumName='plane vis:none', attributeType='enum')
    mc.addAttr(ctrl, cachedInternally=True, shortName='root', longName='root', 
               niceName='Root', enumName='off:on', attributeType='enum')
    mc.addAttr(ctrl, cachedInternally=True, shortName='ctrl', longName='ctrl', 
               niceName='Ctrl', enumName='off:on', attributeType='enum')
    mc.addAttr(ctrl, cachedInternally=True, shortName='lines', longName='lines', 
               niceName='Lines', enumName='off:on', attributeType='enum')
    mc.addAttr(ctrl, cachedInternally=True, shortName='plane', longName='plane', 
               niceName='Plane', enumName='off:on', attributeType='enum')
    mc.addAttr(ctrl, cachedInternally=True, shortName='grid', longName='grid', 
               niceName='Grid', enumName='off:on', attributeType='enum')
    mc.addAttr(ctrl, cachedInternally=True, shortName='dimensions', longName='dimensions', 
               niceName='Dimensions', enumName='off:on', attributeType='enum')
    mc.addAttr(ctrl, cachedInternally=True, shortName='scalePlane', longName='scalePlane', 
               niceName='____________________', enumName='plane scale:none', attributeType='enum')
    mc.addAttr(ctrl, cachedInternally=True, shortName='shortest', longName='shortest', 
               niceName='Shortest', min=0.0, max=3.0, dv=1.0, attributeType='double')
    mc.addAttr(ctrl, cachedInternally=True, shortName='longest', longName='longest', 
               niceName='Longest', min=0.0, max=3.0, dv=1.0, attributeType='double')
    
    mc.setAttr(ctrl+'.root', 1)
    mc.setAttr(ctrl+'.ctrl', 1)
    mc.setAttr(ctrl+'.lines', 1)
    mc.setAttr(ctrl+'.plane', 1)
    mc.setAttr(ctrl+'.grid', 1)
    
    nodes_proxy=['displayPlane', 'root', 'ctrl', 'lines', 'plane', 'grid', 'dimensions', 'scalePlane', 'shortest', 'longest']
    for n in nodes_proxy:
        mc.addAttr(ctrl_A, longName=n, proxy=ctrl+'.'+n)
        mc.addAttr(ctrl_B, longName=n, proxy=ctrl+'.'+n)
        mc.addAttr(ctrl_C, longName=n, proxy=ctrl+'.'+n)
        mc.addAttr(plane, longName=n, proxy=ctrl+'.'+n)

    ###### create guides for display
    ##############################################################################################
    pntCtrl=[(0.6, 0.0, -0.3), (0.6, 0.0, 0.3), (0.3, 0.0, 0.6), 
             (-0.3, 0.0, 0.6), (-0.6, 0.0, 0.3), (-0.6, 0.0, -0.3), 
             (-0.3, 0.0, -0.6), (0.3, 0.0, -0.6), (0.6, 0.0, -0.3)]
    k=[i for i in range(len(pntCtrl))]
    exec('temp=mc.curve(degree=1, p='+str(pntCtrl)+', k='+str(k)+', name=\"dede\")')
    ctrlShape=mc.ls(mc.listRelatives(temp, shapes=True,  noIntermediate=True), type='nurbsCurve')[0]
    ctrl_guide=mc.createNode('guideLineShape', name=p+'_ctrl_guide', parent=ctrl)
    mc.connectAttr(ctrlShape+'.worldSpace[0]', ctrl_guide+'.create', force=True)
    mc.delete(temp)

    ctrl_AC_guide=mc.createNode('guideLineShape', name=p+'_AC_ctrl_guide', parent=ctrl_A)
    ctrl_B_guide=mc.createNode('guideLineShape', name=p+'_B_ctrl_guide', parent=ctrl_B)
    mc.parent(ctrl_AC_guide, ctrl_C, add=True, shape=True)

    distance_guide=mc.createNode('guideLineShape', name=p+'_zero_distance_guide', parent=z)
    shortest_guide=mc.createNode('guideLineShape', name=p+'_zero_shortest_guide', parent=z)

    mc.setAttr(ctrl_guide+'.xRay', True)
    mc.setAttr(ctrl_guide+'.color', 0.513, 0.442, 0.283)

    mc.setAttr(distance_guide+'.xRay', True)
    mc.setAttr(distance_guide+'.template', True)
    mc.setAttr(distance_guide+'.conserveColor', True)
    mc.setAttr(distance_guide+'.color', 0.228, 0.228, 0.228)

    mc.setAttr(shortest_guide+'.xRay', True)
    mc.setAttr(shortest_guide+'.template', True)
    mc.setAttr(shortest_guide+'.conserveColor', True)
    mc.setAttr(shortest_guide+'.color', 0.228, 0.228, 0.228)

    mc.setAttr(ctrl_AC_guide+'.xRay', True)
    mc.setAttr(ctrl_AC_guide+'.conserveColor', True)
    mc.setAttr(ctrl_AC_guide+'.color', 0.671, 0.671, 0.671)

    mc.setAttr(ctrl_B_guide+'.xRay', True)
    mc.setAttr(ctrl_B_guide+'.conserveColor', True)
    mc.setAttr(ctrl_B_guide+'.color', 1.0, 0.385, 0.0)

    ###### create distance curve
    ##############################################################################################
    pntDist=[(-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)]
    k=[i for i in range(len(pntDist))]
    exec('temp=mc.curve(degree=1, p='+str(pntDist)+', k='+str(k)+', name=\"dede\")')
    distShape=mc.ls(mc.listRelatives(temp, shapes=True,  noIntermediate=True), type='nurbsCurve')[0]
    mc.parent(distShape, z, add=True, shape=True)
    distShape=mc.rename(distShape, p+'_zero_distance_curve')
    mc.delete(temp)

    ###### create shortest curve
    ##############################################################################################
    pntShortest=[(0.0, 0.0, 0.0), (0.0, 0.0, -1.0)]
    k=[i for i in range(len(pntShortest))]
    exec('temp=mc.curve(degree=1, p='+str(pntShortest)+', k='+str(k)+', name=\"dede\")')
    shortestShape=mc.ls(mc.listRelatives(temp, shapes=True,  noIntermediate=True), type='nurbsCurve')[0]
    mc.parent(shortestShape, z, add=True, shape=True)
    shortestShape=mc.rename(shortestShape, p+'_zero_shortest_curve')
    mc.delete(temp)

    ###### create curve for A, B, C ctrl
    ##############################################################################################
    pntCtrl_son=[(0.0, 0.0, 0.0), (0.04691, 0.0, 0.0), (0.04691, 0.00607, 0.0), 
                 (0.01676, 0.03352, 0.0), (-0.01676, 0.03352, 0.0), (-0.04691, 0.00607, 0.0), 
                 (-0.04691, -0.00607, 0.0), (-0.01676, -0.03352, 0.0), (0.01676, -0.03352, 0.0), 
                 (0.04691, -0.00607, 0.0), (0.04691, 0.0, 0.0), (0.04691, 0.0, 0.02346), 
                 (0.02346, 0.0, 0.04691), (-0.02346, 0.0, 0.04691), (-0.04691, 0.0, 0.02346), 
                 (-0.04691, 0.0, -0.02346), (-0.02346, 0.0, -0.04691), (0.02346, 0.0, -0.04691), 
                 (0.04691, -0.0, -0.02346), (0.04691, 0.0, 0.0), (0.0, 0.0, 0.0), 
                 (0.0, 0.0, -0.04691), (0.0, 0.00607, -0.04691), (0.0, 0.03352, -0.01676), 
                 (0.0, 0.03352, 0.01676), (0.0, 0.00607, 0.04691), (0.0, -0.00607, 0.04691), 
                 (0.0, -0.03352, 0.01676), (0.0, -0.03352, -0.01676), (0.0, -0.00607, -0.04691), 
                 (0.0, 0.0, -0.04691), (0.0, 0.0, 0.04691), (0.0, 0.0, 0.0), (-0.04691, 0.0, 0.0)]
    k=[i for i in range(len(pntCtrl_son))]
    exec('temp=mc.curve(degree=1, p='+str(pntCtrl_son)+', k='+str(k)+', name=\"dede\")')
    ctrl_sonShape=mc.ls(mc.listRelatives(temp, shapes=True,  noIntermediate=True), type='nurbsCurve')[0]
    mc.parent(ctrl_sonShape, z, add=True, shape=True)
    ctrl_sonShape=mc.rename(ctrl_sonShape, p+'_zero_proxy_guide')
    mc.delete(temp)
    cluster=mc.cluster(ctrl_sonShape)
    mc.parent(cluster[1], z)
    cluster=mc.rename(cluster[1], p+'_zero_proxy_guide_cluster')
    clusterHandle=mc.ls(mc.listHistory(cluster), type='clusterHandle')[0]
    clusterNode=mc.ls(mc.listHistory(ctrl_sonShape), type='cluster')[0]

    tweak=mc.ls(mc.listHistory(ctrl_sonShape), type='tweak')
    mc.delete(tweak)

    ###### create node for compute and display
    ##############################################################################################
    dimensionA=mc.createNode('distanceDimShape', name=p+'_zero_dimensionA', parent=z)
    dimensionB=mc.createNode('distanceDimShape', name=p+'_zero_dimensionB', parent=z)
    dimensionC=mc.createNode('distanceDimShape', name=p+'_zero_dimensionC', parent=z)
    dBA=mc.createNode('distanceBetween', name=p+'_dBA')
    dBB=mc.createNode('distanceBetween', name=p+'_dBB')
    dM=mc.createNode('decomposeMatrix', name=p+'_dM')
    mD=mc.createNode('multDoubleLinear', name=p+'_mD')
    nPOC=mc.createNode('nearestPointOnCurve', name=p+'_nPOC')
    ss_mD=mc.createNode('multDoubleLinear', name=p+'_ss_mD')
    sl_mD=mc.createNode('multDoubleLinear', name=p+'_sl_mD')

    ###### connect guides
    ##############################################################################################
    mc.connectAttr(ctrl_sonShape+'.worldSpace[0]', ctrl_AC_guide+'.create', force=True)
    mc.connectAttr(ctrl_sonShape+'.worldSpace[0]', ctrl_B_guide+'.create', force=True)
    mc.connectAttr(distShape+'.worldSpace[0]', distance_guide+'.create', force=True)
    mc.connectAttr(shortestShape+'.worldSpace[0]', shortest_guide+'.create', force=True)

    ###### connect rigidConstraint
    ##############################################################################################
    mc.connectAttr(ctrl_A_loc+'.worldPosition[0]', rCons+'.pointDrivers[0].inPoint', force=True)
    mc.connectAttr(ctrl_B_loc+'.worldPosition[0]', rCons+'.pointDrivers[1].inPoint', force=True)
    mc.connectAttr(ctrl_C_loc+'.worldPosition[0]', rCons+'.pointDrivers[2].inPoint', force=True)
    mc.setAttr(rCons+'.pointDrivers[0].dvPointX', -1.0)
    mc.setAttr(rCons+'.pointDrivers[1].dvPointZ', -1.0)
    mc.setAttr(rCons+'.pointDrivers[2].dvPointX', 1.0)
    mc.connectAttr(rCons+'.outRotate', cluster+'.rotate', force=True)
    mc.connectAttr(rCons+'.outRotate', plane+'.rotate', force=True)

    ###### pointConstraint plane
    ##############################################################################################
    pConstraint=mc.pointConstraint( ctrl_A, ctrl_C, plane, w=0.5, name=p+'_plane_pCons' )[0]

    ###### connect dimensionA
    ##############################################################################################
    mc.connectAttr(nPOC+'.position', dimensionA+'.startPoint', force=True)
    mc.connectAttr(ctrl_A_loc+'.worldPosition[0]', dimensionA+'.endPoint', force=True)
    mc.setAttr(dimensionA+'.overrideEnabled', 1)
    mc.setAttr(dimensionA+'.overrideDisplayType', 2)

    ###### connect dimensionB
    ##############################################################################################
    mc.connectAttr(ctrl_C_loc+'.worldPosition[0]', dimensionB+'.startPoint', force=True)
    mc.connectAttr(nPOC+'.position', dimensionB+'.endPoint', force=True)
    mc.setAttr(dimensionB+'.overrideEnabled', 1)
    mc.setAttr(dimensionB+'.overrideDisplayType', 2)

    ###### connect dimensionC
    ##############################################################################################
    mc.connectAttr(ctrl_B_loc+'.worldPosition[0]', dimensionC+'.startPoint', force=True)
    mc.connectAttr(nPOC+'.position', dimensionC+'.endPoint', force=True)
    mc.setAttr(dimensionC+'.overrideEnabled', 1)
    mc.setAttr(dimensionC+'.overrideDisplayType', 2)

    ###### connect distance Shape
    ##############################################################################################
    mc.connectAttr(ctrl_A_loc+'.worldPosition[0]', distShape+'.cp[0]', force=True)
    mc.connectAttr(ctrl_C_loc+'.worldPosition[0]', distShape+'.cp[1]', force=True)

    ###### connect shortest Shape
    ##############################################################################################
    mc.connectAttr(nPOC+'.position', shortestShape+'.cp[0]', force=True)
    mc.connectAttr(ctrl_B_loc+'.worldPosition[0]', shortestShape+'.cp[1]', force=True)

    ###### connect dBA
    ##############################################################################################
    mc.connectAttr(ctrl_A_loc+'.worldPosition[0]', dBA+'.point1', force=True)
    mc.connectAttr(ctrl_C_loc+'.worldPosition[0]', dBA+'.point2', force=True)
    mc.connectAttr(dBA+'.distance', mD+'.input1', force=True)

    ###### connect dBB
    ##############################################################################################
    mc.connectAttr(ctrl_B_loc+'.worldPosition[0]', dBB+'.point1', force=True)
    mc.connectAttr(nPOC+'.position', dBB+'.point2', force=True)

    ###### connect mD
    ##############################################################################################    
    mc.setAttr(mD+'.input2', 0.5)

    ###### connect nPOC
    ##############################################################################################
    mc.connectAttr(ctrl_B_loc+'.worldPosition[0]', nPOC+'.inPosition', force=True)
    mc.connectAttr(distShape+'.worldSpace[0]', nPOC+'.inputCurve', force=True)

    ###### connect dM
    ##############################################################################################
    mc.connectAttr(ctrl+'.inverseMatrix', dM+'.inputMatrix', force=True)
    mc.connectAttr(dM+'.outputRotate', ctrl_A+'.rotate', force=True)
    mc.connectAttr(dM+'.outputRotate', ctrl_B+'.rotate', force=True)
    mc.connectAttr(dM+'.outputRotate', ctrl_C+'.rotate', force=True)

    ###### connect ss_mD
    ##############################################################################################
    mc.connectAttr(mD+'.output', ss_mD+'.input1')
    mc.connectAttr(ctrl+'.longest', ss_mD+'.input2')
    mc.connectAttr(ss_mD+'.output', plane+'.scaleX', force=True)

    ###### connect sl_mD
    ##############################################################################################
    mc.connectAttr(dBB+'.distance', sl_mD+'.input1')
    mc.connectAttr(ctrl+'.shortest', sl_mD+'.input2')
    mc.connectAttr(sl_mD+'.output', plane+'.scaleZ', force=True)

    ###### connect visibility
    ##############################################################################################
    mc.connectAttr(ctrl+'.root', ctrl_guide+'.v')
    mc.connectAttr(ctrl+'.ctrl', ctrl_AC_guide+'.v')
    mc.connectAttr(ctrl+'.ctrl', ctrl_B_guide+'.v')
    mc.connectAttr(ctrl+'.lines', distance_guide+'.v')
    mc.connectAttr(ctrl+'.lines', shortest_guide+'.v')
    mc.connectAttr(ctrl+'.plane', planeShape+'.v')
    mc.connectAttr(ctrl+'.grid', gridShape+'.v')
    mc.connectAttr(ctrl+'.dimensions', dimensionA+'.v')
    mc.connectAttr(ctrl+'.dimensions', dimensionB+'.v')
    mc.connectAttr(ctrl+'.dimensions', dimensionC+'.v')

    ###### manage interface visibility
    ##############################################################################################
    
    hiddenCB = [planeShape, gridShape, pConstraint, rCons, dimensionA, dimensionB, dimensionC,
                dBA, dBB, mD, dM, nPOC, ss_mD, sl_mD, distance_guide, shortest_guide, cluster, 
                clusterHandle, clusterNode, distShape, shortestShape, ctrl_sonShape, ctrl_guide,
                ctrl_A_loc, ctrl_B_loc, ctrl_C_loc, ctrl_AC_guide, ctrl_B_guide, z]
    for h in hiddenCB:
        mc.setAttr(h+'.isHistoricallyInteresting', False)


    hiddenInOutliner = [planeShape, gridShape, pConstraint, rCons, dimensionA, dimensionB, dimensionC, 
                        distance_guide, shortest_guide, cluster, clusterHandle, distShape, shortestShape,
                        ctrl_sonShape, ctrl_guide, ctrl_A_loc, ctrl_B_loc, ctrl_C_loc, ctrl_AC_guide, ctrl_B_guide, z]
    for h in hiddenInOutliner:
        mc.setAttr(h+'.hiddenInOutliner', True)
    
    hiddenNode=[cluster, ctrl_A_loc, ctrl_B_loc, ctrl_C_loc, distShape, shortestShape, ctrl_sonShape]
    for h in hiddenNode:
        mc.setAttr(h+'.v', False)

    noChannelBox_t=[plane, rCons, z, cluster]
    for noCB in noChannelBox_t:
        mc.setAttr(noCB+'.tx', keyable=False, channelBox=False)
        mc.setAttr(noCB+'.ty', keyable=False, channelBox=False)
        mc.setAttr(noCB+'.tz', keyable=False, channelBox=False)

    noChannelBox_r_s=[plane, rCons, z, cluster, ctrl_A, ctrl_B, ctrl_C]
    for noCB in noChannelBox_r_s:
        mc.setAttr(noCB+'.rx', keyable=False, channelBox=False)
        mc.setAttr(noCB+'.ry', keyable=False, channelBox=False)
        mc.setAttr(noCB+'.rz', keyable=False, channelBox=False)
        mc.setAttr(noCB+'.sx', keyable=False, channelBox=False)
        mc.setAttr(noCB+'.sy', keyable=False, channelBox=False)
        mc.setAttr(noCB+'.sz', keyable=False, channelBox=False)        

    noChannelBox_v=[plane, z, cluster]
    for noCB in noChannelBox_v:
        mc.setAttr(noCB+'.v', keyable=False, channelBox=False)

    noChannelBox_attr=['.root', '.ctrl', '.lines', '.plane', '.grid', '.dimensions', '.shortest', '.longest']
    for noCB in noChannelBox_attr:
        mc.setAttr(ctrl+noCB, keyable=True)

    noChannelBox_attr2=['.displayPlane', '.scalePlane']
    for noCB in noChannelBox_attr2:
        mc.setAttr(ctrl+noCB, keyable=False, channelBox=True)
    
    ###### lock attr
    ##############################################################################################
    lock_attrs_t=[plane, rCons, z, cluster]
    for l in lock_attrs_t:
        mc.setAttr(l+'.tx', lock=True)
        mc.setAttr(l+'.ty', lock=True)
        mc.setAttr(l+'.tz', lock=True)

    lock_attrs_r_s=[plane, rCons, z, cluster, ctrl_A, ctrl_B, ctrl_C]
    for l in lock_attrs_r_s:
        mc.setAttr(l+'.rx', lock=True)
        mc.setAttr(l+'.ry', lock=True)
        mc.setAttr(l+'.rz', lock=True)
        mc.setAttr(l+'.sx', lock=True)
        mc.setAttr(l+'.sy', lock=True)
        mc.setAttr(l+'.sz', lock=True)

    lock_attrs_v=[plane, planeShape, gridShape, z, distance_guide, shortest_guide, distShape, shortestShape, ctrl_sonShape,
                  dimensionA, dimensionB, dimensionC, ctrl_guide, ctrl_AC_guide, ctrl_B_guide, cluster]
    for l in lock_attrs_t:
        mc.setAttr(l+'.v', lock=True)
    
    mc.setAttr(mD+'.input2', lock=True)

    lock_attr_user=['.displayPlane', '.scalePlane']
    for noCB in lock_attr_user:
        mc.setAttr(ctrl+noCB, lock=True)

    ###### list node for further use
    ##############################################################################################
    listNode={}
    listNode['ctrl']=[ctrl, ctrl_A, ctrl_B, ctrl_C]
    listNode['ctrlShape']=[ctrl_A_loc, ctrl_B_loc, ctrl_C_loc, ctrl_guide, ctrl_B_guide, ctrl_AC_guide]
    listNode['plane']=[plane]
    listNode['planeShape']=[planeShape, gridShape, rCons, pConstraint]
    listNode['shader']=[planeShader, planeShaderSG]
    listNode['zero']=[z]
    listNode['zeroShape']=[distance_guide, shortest_guide, distShape, shortestShape, ctrl_sonShape, cluster, clusterHandle, clusterNode,
                           dimensionA, dimensionB, dimensionC]
    listNode['compute']=[dBA, dBB, dM, mD, nPOC, ss_mD, sl_mD]

    nodesPlane=[ctrl, ctrl_A, ctrl_B, ctrl_C, 
                ctrl_A_loc, ctrl_B_loc, ctrl_C_loc, ctrl_guide, ctrl_B_guide, ctrl_AC_guide,
                plane,
                planeShape, gridShape, rCons, pConstraint,
                planeShader, planeShaderSG,
                z,
                distance_guide, shortest_guide, distShape, shortestShape, ctrl_sonShape,
                cluster, clusterHandle, clusterNode,
                dimensionA, dimensionB, dimensionC,
                dBA, dBB, dM, mD, nPOC, ss_mD, sl_mD]
    for np in nodesPlane:
        mc.addAttr(np, longName='listNode', dataType='string')
        mc.setAttr(np+'.listNode', repr(listNode), type='string')
        mc.setAttr(np+'.listNode', lock=True)

    return ctrl, ctrl_A, ctrl_B, ctrl_C, plane, planeShape



def loadPlugins():
    require_plugin = ['rigidConstraint', 'guideLineShape2016']
    for plugin in require_plugin:
        if not mc.pluginInfo(plugin, q=True, l=True):
            try:
                mc.loadPlugin(plugin, quiet=True)
            except:
                mc.error(plugin+' plugin can not load')
                break


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    '''
    Python 2 implementation of Python 3.5 math.isclose()
    https://hg.python.org/cpython/file/tip/Modules/mathmodule.c#l1993
    '''
    # sanity check on the inputs
    if rel_tol < 0 or abs_tol < 0:
        raise ValueError("tolerances must be non-negative")

    # short circuit exact equality -- needed to catch two infinities of
    # the same sign. And perhaps speeds things up a bit sometimes.
    if a == b:
        return True

    # This catches the case of two infinities of opposite sign, or
    # one infinity and one finite number. Two infinities of opposite
    # sign would otherwise have an infinite relative tolerance.
    # Two infinities of the same sign are caught by the equality check
    # above.
    if math.isinf(a) or math.isinf(b):
        return False

    # now do the regular computation
    # this is essentially the "weak" test from the Boost library
    diff = math.fabs(b - a)
    result = (((diff <= math.fabs(rel_tol * b)) or
               (diff <= math.fabs(rel_tol * a))) or
              (diff <= abs_tol))
    return result

def barycentre(argSelection, argRound):
    '''
    input : shape and accurancy
    output : exact center of all vertices of shape, this method is differently of min/max of bounding box, the weight of vertices change the result
    '''
    datas = mc.xform('{0}.cp[*]'.format(argSelection), t=True, query=True, ws=True)
    datas =[round(cp, argRound) for cp in datas]
    dts = zip(*list([iter(datas)] * 3))
    divider = len(dts)
    x = 0.0
    y = 0.0
    z = 0.0    
    for i in range(divider):
        x+=dts[i][0]
        y+=dts[i][1]
        z+=dts[i][2]
    return [round(x/divider, argRound), round(y/divider, argRound), round(z/divider, argRound)], dts

def distance(argA, argB, argRound):
    '''
    give two tuple or list
    '''
    return round(math.sqrt((argA[0] - argB[0]) ** 2 + (argA[1] - argB[1]) ** 2 + (argA[2] - argB[2]) ** 2), argRound)

def distance2D(argA, argB):
    '''
    give two tuple or list
    '''
    return math.sqrt((argA[0] - argB[0]) ** 2 + (argA[1] - argB[1]) ** 2)



