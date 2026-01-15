from config.settings import FACE_MIN_AREA_RATIO, FACE_MAX_AREA_RATIO

def is_face_distance_valid(face, frame_shape):
    x, y, w, h = face
    frame_area = frame_shape[0] * frame_shape[1]
    face_area = w * h
    ratio = face_area / frame_area
    return FACE_MIN_AREA_RATIO <= ratio <= FACE_MAX_AREA_RATIO
