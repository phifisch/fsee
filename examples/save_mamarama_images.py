import os, math, glob
import pickle

import cgkit.cgtypes as cgtypes # cgkit 2.x

import fsee
import fsee.Observer

import numpy
import scipy.io
import pylab
import fsee.eye_geometry.util
import fsee.plot_utils

class PathMaker:
    def __init__(self,
                 pos_0=cgtypes.vec3(0,0,0),
                 ori_0=cgtypes.quat(1,0,0,0),
                 vel_0=cgtypes.vec3(0,0,0),
                 ):
        self.pos_0 = pos_0
        self.ori_0 = ori_0
        self.vel_0 = vel_0
        self.reset()
    def reset(self):
        self.cur_pos = self.pos_0
        self.cur_ori = self.ori_0
        self.vel = self.vel_0
        self.angular_vel = cgtypes.vec3(0,0,0) # fixed for now
        self.last_t = None
    def step(self,t):
        if self.last_t is not None:
            delta_t = t-self.last_t
        else:
            delta_t = 0
        self.last_t = t
        self.cur_pos += self.vel*delta_t

        return self.cur_pos, self.cur_ori, self.vel, self.angular_vel

def main():
    model_path = os.path.join(
            fsee.data_dir,"models/mamarama_checkerboard/mamarama_checkerboard.osg") # trigger extraction

    hz = 100.0
    dt = 1/hz
    vision = None

    path_maker = PathMaker(vel_0=cgtypes.vec3(400,0,0),
                           pos_0=cgtypes.vec3(000,200,150))

    if 1:
        if 1:
            vision = fsee.Observer.Observer(model_path=model_path,
                                            scale=1000.0, # convert model from meters to mm
                                            hz=hz,
                                            skybox_basename=None,
                                            full_spectrum=True,
                                            optics='buchner71',
                                            do_luminance_adaptation=False,
                                            )
            t = -dt
            count = 0
            while count<250:
                t+=dt
                count += 1

                cur_pos = None
                cur_ori = None
                cur_pos, cur_ori, vel, angular_vel = path_maker.step(t)
                vision.step(cur_pos,cur_ori)

                #vision.save_last_environment_map('mamarama_envmap%03d.png'%count)

                if 0 and (count-1)%100==0:
                    EMDs = vision.get_last_emd_outputs()
                    R = vision.get_last_retinal_imageR()
                    G = vision.get_last_retinal_imageG()
                    B = vision.get_last_retinal_imageB()

                    fname = 'mamarama_receptors_%04d'%(count,)

                    fsee.plot_utils.plot_receptor_and_emd_fig(
                        R=R,G=G,B=B,
                        emds=EMDs,
                        scale=1e-3,
                        figsize=(10,10),
                        dpi=100,
                        save_fname=fname+'.png',
                        optics=vision.get_optics(),
                        proj='stere',
                        )
                    if 1:
                        fsee.plot_utils.plot_receptor_and_emd_fig(
                            R=R,G=G,B=B,
                            emds=EMDs,
                            scale=5e-3,
                            figsize=(10,10),
                            dpi=100,
                            save_fname=fname+'.pdf',
                            optics=vision.get_optics(),
                            proj='stere',
                            )
if 1:
    main()
