leds_per_ring = 300

TWINKLE_LEDS_PER_TREE = 300
RAIN_INITIAL_LIT_LEDS_PER_TREE = 300

PD_TREE_PORT_PREFIX = 6000
PYTHON_CONTROL_PORT = 4000

SHOW_FPS = False

SHOW_LAST_UPDATE = False

# PROTOCOL = "TCP"
PROTOCOL = "UDP"

# for looping call interval
TARGET_FPS = 40

ENABLE_NETWORKING = True

# -------------------------------------------------------------------------------
# fixme
AUDIO_PC_IP = '10.0.0.34'
AUDIO_PC_PORT = 6011
# -------------------------------------------------------------------------------

trees_config = [{'host': '0.0.0.0:7891', 'channel': 0, 'default_mode': 9, 'pd_port': AUDIO_PC_PORT}]


mode_str_to_int = {
	'rain': 4,
	'chant1': [7],
	'laserFire': [5, 6, 8],
	# 'spaceLong': [5, 6, 8],
	# 'spaceLaserTest': [5, 6, 8],
	# 'spaceLaser': [5, 6, 8],
}

chant_file_to_color = {
	"chant1inA.wav": (219, 148, 255),
	"chant1inC.wav": (113, 152, 232),
	"chant1inD.wav": (137, 255, 217),
	"chant1inF#.wav": (183, 232, 143),
	"chant1inG.wav": (255, 230, 137),
}

sound_file_envelops = {
	"011113_slinky-quotpewquot-laser-sound-59279.wav": [500, 1535],
	"analog-lazer-fx-87122.wav": [823, 1289],
	"blaster1.wav": [378, 563],
	"blaster2.wav": [372, 571],
	"blaster3.wav": [714, 908],
	"boomerang-128276.wav": [382, 1885],
	"edm-laser-140951.wav": [2606, 7627],
	"heavy-beam-weapon-7052.wav": [1333, 4278],
	"laser-cannon-science-fiction-sound-9831-1.wav": [1655, 1235],
	"laser-cannon-science-fiction-sound-9831-2.wav": [1778, 3305],
	"laser_falling-104772.wav": [940, 5996],
	"laser-gun-72558-1.wav": [158, 181],
	"laser-gun-72558-2.wav": [230, 219],
	"laser-gun-81720.wav": [340, 1797],
	"laser-whoosh-37530.wav": [1559, 1729],
	"power-down-7103.wav": [356, 1468],
	"shoot02wav-14562.wav": [152, 200],
}

