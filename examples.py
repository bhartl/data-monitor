import time
import numpy as np
from itertools import count
from data_monitor import DataMonitor


def get_sample(index):
    """ generate sample data based on a itertools.count() instance """

    t = next(index)

    data = [
        t,
        np.cos(t * np.pi * 2. / 30.) + 1 + np.random.rand() * 0.25 - 0.125,
        np.sin(t * np.pi * 2. / 30.) - 1 + np.random.rand() * 0.25 - 0.125,
    ]

    return data


def data_monitor(n_steps: int = 150, sleep_time: float = 0.01):
    """ show noisy sine-wave data on a DataMonitor

    :param n_steps:  number of produced data points (and updates in the DataMonitor)
    :param sleep_time:  delay time between data-poin generation
    """

    # generate itertools.count instance
    index = count()

    # get temporal data
    sample = get_sample(index=index)
    data = [sample]

    # define meta-info for DataMonitor plotting (label of data-rows and coloring)
    channels = [
        {'label': 'Channel 1'},
        {'label': 'Channel 2', 'color': 'tab:orange'},
    ]

    # define plot format (dict of matplotlib.pyplot attributes and related (*args, **kwargs))
    plt_kwargs = dict(
        xlim=((0, n_steps), {}),
        ylim=((-2.5, 2.5), {}),
        xlabel=(('steps', ), {}),
        ylabel=(('values',), {}),
    )

    # start DataMonitor in with environment:
    # - the monitor starts a background process which needs to be closed at the end,
    #   `with` takes care of this
    with DataMonitor(channels=channels, ax_kwargs=plt_kwargs) as dm:

        for i in range(1, n_steps):

            # pull next sample data
            sample = get_sample(index)
            data.append(sample)

            # update the data-monitor (row-wise data: (x, y1, y2))
            dm.data = np.asarray(data).T

            # apply delay
            time.sleep(sleep_time)

    print('done')


def nonblocking_plot(n_steps: int = 150, sleep_time: float = 0.01):
    """ show noisy sine-wave data on a DataMonitor

    :param n_steps:  number of produced data points (and updates in the DataMonitor)
    :param sleep_time:  delay time between data-poin generation
    """

    # generate itertools.count instance
    index = count()

    # get ALL temporal data
    sample = get_sample(index=index)
    data = [sample]

    for i in range(1, n_steps):
        # pull next sample data
        sample = get_sample(index)
        data.append(sample)

    data = np.asarray(data).T

    # define meta-info for DataMonitor plotting (label of data-rows and coloring)
    channels = [
        {'label': 'Channel 1'},
        {'label': 'Channel 2', 'color': 'tab:orange'},
    ]

    # define plot format (dict of matplotlib.pyplot attributes and related (*args, **kwargs))
    plt_kwargs = dict(
        xlim=((0, n_steps), {}),
        ylim=((-2.5, 2.5), {}),
        xlabel=(('steps', ), {}),
        ylabel=(('values',), {}),
    )

    # start DataMonitor in with environment:
    # - the monitor starts a background process which needs to be closed at the end,
    #   `with` takes care of this
    with DataMonitor(data=data, channels=channels, ax_kwargs=plt_kwargs):

        print('non-blocking plot, do something else ...')
        pass

    print('done')


def custom_axes_monitor(n_steps: int = 150, sleep_time: float = 0.01):
    """ show noisy sine-wave data on a **custom** DataMonitor

    :param n_steps:  number of produced data points (and updates in the DataMonitor)
    :param sleep_time:  delay time between data-poin generation
    """

    import matplotlib.pyplot as plt

    # define, how figure and axes are generated: generate two axes
    def make_fig(**kwargs):
        fig, (ax_0, ax_1) = plt.subplots(2, 1, sharex=True, **kwargs)
        return fig, (ax_0, ax_1)

    # define, how data (x, y1, x2) is plotted on axes
    def axes_plot(ax, data, channels):
        x, y1, y2 = data

        ax[0].plot(x, y1, **channels[0])
        ax[1].plot(x, y2, **channels[1])

    # show legend in each subplot
    def legend(ax, channels):
        for ax_i in ax:
            ax_i.legend()

    # generate data
    index = count()
    sample = get_sample(index)
    data = [sample]

    # define channel meta-info
    channels = [
        {'label': 'Channel 1'},
        {'label': 'Channel 2', 'color': 'tab:orange'},
    ]

    # define format instructions for both axes (we avoid an xlabel in the top axis)
    ax_kwargs = [
        dict(set_xlim=((0, n_steps), {}), set_ylim=((-0.5, 2.5), {}), set_ylabel=(('values',), {})),
        dict(set_xlim=((0, n_steps), {}), set_ylim=((-2.5, 0.5), {}), set_ylabel=(('values',), {}), set_xlabel=(('steps', ), {}))
    ]

    # start DataMonitor in with environment:
    # - the monitor starts a background process which needs to be closed at the end,
    #   `with` takes care of this
    with DataMonitor(make_fig=make_fig,  # define, how figure and axes are generated
                     make_fig_kwargs={'figsize': (10, 10)},  # kwargs in figure generation (optional)
                     ax_plot=axes_plot,  # define, how data is plotted on axes
                     channels=channels,  # define kwargs for each data row
                     ax_kwargs=ax_kwargs,  # define axes labeling/formatting
                     legend=legend,  # define, how legend is generated
                     update_rate=1.,
                     ) as dm:

        for i in range(1, n_steps):
            # pull next sample data
            sample = get_sample(index)
            data.append(sample)

            # update the data-monitor (row-wise data: (x, y1, y2))
            dm.data = np.asarray(data).T

            # apply delay
            time.sleep(sleep_time)

    print('done')


if __name__ == '__main__':
    import argh
    argh.dispatch_commands([data_monitor,
                            nonblocking_plot,
                            custom_axes_monitor,
                            ])
