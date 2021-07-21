def transmissivity(index_pre, index_post):
    return 1 - ((index_post - index_pre)/(index_post + index_pre)) ** 2

def reflectivity(index_pre, index_post):
    return ((index_post - index_pre)/(index_post + index_pre)) ** 2

class medium:
    def __init__(self, width, index):
        self.width = width
        self.index = index

dims = (
    medium(1, 1),
    medium(1, 1.47),
    medium(1, 1.3),
)

def main(min, dimensions):

    final_state = [0, 0] # [left side, right side]

    amplitude = 1
    position = 0
    dir = True # direction the light is travelling
    count = 0

    def dir_pretty(dir):
        return ('left', 'right')[dir]

    def get_index(position):
        return dimensions[position].index

    def junction(final_state, amplitude, position, dir, count):
        print('  (@{}, travelling {}, init_a {}) Entering junction'.format(position, dir_pretty(dir), amplitude))

        pre_index = get_index((position + 1, position)[dir])
        post_index = get_index((position, position + 1)[dir])

        count += 1
        if count > 30:
            print ('count exceeded')
            return

        def reflection(): #The outcomes for if a reflection occurs at an intersection
            ref_dir = not dir

            amplitude_ref = amplitude * reflectivity(pre_index, post_index)

            if (amplitude_ref < min):
                print('  (@{}, travelling {}, init_a {}) Too small reflection:'.format(position, dir_pretty(ref_dir), amplitude, amplitude_ref))
                return
            elif (position == 0 and not ref_dir):
                print("    (@{}, travelling {}, init_a {}) adding to REF SUM: {}".format(position, dir_pretty(ref_dir), amplitude, amplitude_ref))
                final_state[0] += amplitude_ref
            elif (position == len(dimensions) - 2 and ref_dir): # This should never fire, right?
                print("    YOU SHOULDN'T BE HERE, but adding to TRANS SUM:", amplitude_ref)
                final_state[1] += amplitude_ref
            else:
                ref_position = position + (1, -1)[dir]
                junction(final_state, amplitude_ref, ref_position, ref_dir, count)

        def transmission(): #The outcomes for if a transmission occurs at an intersection
            amplitude_trans = amplitude * transmissivity(pre_index, post_index)

            if(position > len(dimensions) - 2):
                print('ERROR: Position limit exceeded!')
                return

            if amplitude_trans < min:
                print(' Too small transmission:', amplitude_trans)
                return
            elif (position == len(dimensions) - 2 and dir):
                print("    (@{}, travelling {}, init_a {}) adding to TRANS SUM: {}".format(position, dir_pretty(dir), amplitude, amplitude_trans))
                final_state[1] += amplitude_trans
            elif (position == 0) and not dir:
                print("    (@{}, travelling {}, init_a {}) adding to REF SUM:{}".format(position, dir_pretty(dir), amplitude, amplitude_trans))
                final_state[0] += amplitude_trans
            else:
                new_position = position + (-1, 1)[dir]
                junction(final_state, amplitude_trans, new_position, dir, count)

        reflection()
        transmission()

        return final_state

    return junction(final_state, amplitude, position, dir, count)

results = main(0.001, dims)
print('RESULTS:', results)