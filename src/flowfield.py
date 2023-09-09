import numpy
import opensimplex
import PIL.Image
import PIL.ImageDraw
import aggdraw

if __name__ == '__main__':
    width = 384
    height = 216
    opensimplex.seed(2106)
    noise1 = ((opensimplex.noise2array(numpy.linspace(0, 2, width), numpy.linspace(0, 2, height)) + 1) / 2) * 255
    noise2 = ((opensimplex.noise2array(numpy.linspace(0, 8, width), numpy.linspace(0, 8, height)) + 1) / 2) * 255
    noise = (noise1 + noise2) / 2
    noise_img = PIL.Image.fromarray(numpy.uint8(noise), 'L').resize((width * 10, height * 10))
    flowfield_img = PIL.Image.new(size=(3840, 2160), mode='RGBA', color='#000000FF')
    canvas = PIL.ImageDraw.Draw(flowfield_img)
    rng = numpy.random.default_rng(2106)
    jitter = 16
    flows = 2048
    for i in range(int(round(flows ** 0.5))):
        for j in range(int(round(flows ** 0.5))):
            tmp_img = PIL.Image.new(size=(3840, 2160), mode='RGBA', color=(255, 255, 255, 0))
            tmp_canvas = PIL.ImageDraw.Draw(tmp_img)
            # x = rng.integers(0, width * 10)
            # y = rng.integers(0, height * 10)
            x = i * width * 10 // int(round(flows ** 0.5))
            y = j * height * 10 // int(round(flows ** 0.5))
            vertices = list()
            ox = rng.integers(-3 * jitter, 3 * jitter)
            oy = rng.integers(-3 * jitter, 3 * jitter)
            for _ in range (rng.integers(128, 2048)):
                vertices.append((int(round(x)), int(round(y))))

                jx = x + rng.integers(-jitter, jitter) + ox
                jy = y + rng.integers(-jitter, jitter) + oy
                if jx < 0 or jx >= width * 10:
                    jx = x
                if jy < 0 or jy >= height * 10:
                    jy = y
                direction = noise_img.getpixel((jx, jy))
                theta = numpy.deg2rad(direction / 255 * 720)
                x += numpy.cos(theta)
                y += numpy.sin(theta)

                if x < 0 or x >= width * 10 or y < 0 or y >= height * 10:
                    break  

            colors = ['#31393C88', '#2176FF88', '#33A1FD88', '#FDCA4088', '#F7982488']
            #colors = ['#DBB3B188', '#C89FA388', '#A67F8E88', '#6C534E88', '#2C1A1D88']
            #colors = ['#62726488', '#82A08688', '#A1CDA888', '#ABD6B988', '#B5DFCA88', '#BDE3D688', '#C5E7E288']
            # colors = ['#3E564188', '#70503C88', '#A2493688', '#BB553688','#D3613588', '#7E462F88', '#56746988', '#83BCA988']
            fill_color = colors[rng.integers(0, len(colors))]
            line_width = rng.integers(4, 24)
            tmp_canvas.ellipse((vertices[0][0] - line_width // 2, vertices[0][1] - line_width // 2, vertices[0][0] + line_width // 2, vertices[0][1] + line_width // 2), fill=fill_color, outline=None)
            tmp_canvas.ellipse((vertices[-1][0] - line_width // 2, vertices[-1][1] - line_width // 2, vertices[-1][0] + line_width // 2, vertices[-1][1] + line_width // 2), fill=fill_color, outline=None)
            tmp_canvas.line(vertices, fill=fill_color, width=line_width, joint='curve')
            flowfield_img = PIL.Image.alpha_composite(flowfield_img, tmp_img)
    flowfield_img.show()
    flowfield_img.save('flowfield.png')