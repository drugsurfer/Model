import numpy as np
import pandas as pd

import sys
sys.path.append('dz/phase_portrait/src')

from object_data import ControlObject
from sud_data_class import MotionControlSystem

import parser_data as parser_data


def init_control_object(data: pd.DataFrame) -> None:
    """
    Инициализирует параметры объекта управления,
    считанные из таблицы с исходными данными

    Parameters
    ----------
    data : pd.DataFrame
        Таблица с исходными данными
    """
    ControlObject.height, ControlObject.inclination_orbit = (
        parser_data.get_param_of_orbit(data)
    )

    ControlObject.tensor_inertia = parser_data.get_tensor_inertia(data)

    ControlObject.aerodynamic_shoulder_vector = (
        parser_data.get_shoulders_vectors(data)[0]
    )
    ControlObject.sun_pressure_shoulder_vector = (
        parser_data.get_shoulders_vectors(data)[1]
    )
    ControlObject.magnetic_moment = parser_data.get_magnetic_moment(data)

    angles_data = parser_data.get_initial_values(data)
    ControlObject.gamma_angles = np.append(ControlObject.gamma_angles, angles_data["gamma"])
    ControlObject.psi_angles = np.append(ControlObject.psi_angles, angles_data["psi"])
    ControlObject.nu_angles = np.append(ControlObject.nu_angles, angles_data["nu"])
    ControlObject.gamma_w = np.append(ControlObject.gamma_w, angles_data["gamma_w"])
    ControlObject.psi_w = np.append(ControlObject.psi_w, angles_data["psi_w"])
    ControlObject.nu_w = np.append(ControlObject.nu_w, angles_data["nu_w"])
    ControlObject.argument_perigee = np.append(ControlObject.argument_perigee, angles_data["arg_perigee"])


def init_motion_control_system(data: pd.DataFrame) -> None:
    """
    Инициализирует параметры системы управления,
    считанные из таблицы с исходными данными

    Parameters
    ----------
    data : pd.DataFrame
        Таблица с исходными данными
    """
    motion_control_param = parser_data.get_motion_control_param(data)
    MotionControlSystem.alpha = motion_control_param["alpha"] * 180/np.pi
    MotionControlSystem.h = motion_control_param["h"] * 180/np.pi
    MotionControlSystem.k = motion_control_param["k"]
    MotionControlSystem.set_g_effectiveness()
    MotionControlSystem.set_a_effectiveness(parser_data.get_control_moment(data))
    MotionControlSystem.channel_name = parser_data.get_channel_name(data)

def init_objects(file_path: str) -> None:
    """
    Функция инициализации объектов

    Parameters
    ----------
    file_path : str
        Путь до xls файла с исходными данными
    """
    data_file = parser_data.start_read_data(file_path)
    init_control_object(data_file)
    init_motion_control_system(data_file)
