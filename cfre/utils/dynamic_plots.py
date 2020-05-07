from dataclasses import dataclass
from typing import Tuple, Optional, Sequence

import numpy as np
from matplotlib import pyplot as plt


@dataclass
class SubplotConfig:
    title: str
    x_range: Optional[Tuple[float, float]] = None
    y_range: Optional[Tuple[float, float]] = None


class DynamicPlot:

    def __init__(self, subplot_configs: Sequence[SubplotConfig]):
        plt.ion()
        self._figure, self._axs = plt.subplots(len(subplot_configs))
        self._lines = [ax.plot([], [])[0] for ax in self._axs]

        for ax, config in zip(self._axs, subplot_configs):
            ax.set_title(config.title)
            if config.x_range is None:
                ax.set_autoscalex_on(True)
            else:
                ax.set_xlim(*config.x_range)

            if config.y_range is None:
                ax.set_autoscaley_on(True)
            else:
                ax.set_ylim(*config.y_range)


    def update(self, xs: Sequence[float], ys: Sequence[float]):
        for line, x, y in zip(self._lines, xs, ys):
            xdata = np.append(line.get_xdata(), x)
            line.set_xdata(xdata)

            ydata = np.append(line.get_ydata(), y)
            line.set_ydata(ydata)

        for ax in self._axs:
            ax.relim()
            ax.autoscale_view()

        self._figure.canvas.draw()
        self._figure.canvas.flush_events()