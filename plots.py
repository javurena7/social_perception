import matplotlib.pyplot as plt; plt.ion()
import pandas as pd
import numpy as np
import seaborn as sns

def plot_homophilies(path='homophilies/', baseline_correction=False, baseline=False):
    df = pd.read_csv(path + 'summary.txt', sep=' ')
    fig, axs = plt.subplots(1, 2, figsize=(6.3, 3))

    cv = 0. if baseline else .95
    df_a = df[df.cv == cv].pivot("sa", "sb", "bias_a")
    df_b = df[df.cv == cv].pivot("sa", "sb", "bias_b")

    figname = 'figures/homophilies' if not baseline else 'figures/homophilies_baseline'
    center = 1
    vmin = vmax = None
    if baseline_correction:
        df_a0 = df[df.cv == 0].pivot("sa", "sb", "bias_a")
        df_b0 = df[df.cv == 0].pivot("sa", "sb", "bias_b")

        df_a = (df_a - df_a0)
        df_b = (df_b - df_b0)
        center = 0
        figname += '_amplification'

    #vmin = min(df_a.min().min(), df_b.min().min())
    #vmax = max(df_a.max().max(), df_b.max().max())

    sns.heatmap(df_a, cmap='coolwarm', center=center, ax=axs[0], vmin=vmin, vmax=vmax)
    axs[0].invert_yaxis()
    axs[0].set_title('Minority')

    sns.heatmap(df_b, cmap='coolwarm', center=center, ax=axs[1], vmin=vmin, vmax=vmax)
    axs[1].invert_yaxis()
    axs[1].set_title('Majority')

    fig.tight_layout()
    fig.savefig(figname + '.pdf')


def plot_homophily_triadic(path='homophily_triadic/', baseline_correction=False):
    df = pd.read_csv(path + 'summary.txt', sep=' ')
    fig, axs = plt.subplots(1, 2, figsize=(6.3, 3))

    df_a = df.pivot("cv", "sa", "bias_a")
    df_b = df.pivot("cv", "sa", "bias_b")

    df_a0 = df_a.loc[0., :]
    df_b0 = df_b.loc[0., :]

    df_a.drop(0.0, axis=0, inplace=True)
    df_b.drop(0.0, axis=0, inplace=True)

    figname = 'figures/homophily_triadic'
    center = 1
    vmin = vmax = None
    if baseline_correction:
        df_a = df_a - df_a0
        df_b = df_b - df_b0
        center = 0
        figname += '_amplification'

        #vmin = min(df_a.min().min(), df_b.min().min())
        #vmax = max(df_a.max().max(), df_b.max().max())

    sns.heatmap(df_a, cmap='coolwarm', center=center, ax=axs[0], vmin=vmin, vmax=vmax)
    axs[0].invert_yaxis()
    axs[0].set_title('Minority')

    sns.heatmap(df_b, cmap='coolwarm', center=center, ax=axs[1], vmin=vmin, vmax=vmax)
    axs[1].invert_yaxis()
    axs[1].set_title('Majority')

    fig.tight_layout()
    fig.savefig(figname + '.pdf')


def plot_homophily_perception(path='homophily_perception/', baseline_correction=False, log=False):
    df = pd.read_csv(path + 'summary.txt', sep=' ')
    cvs = [.2, .5, .7, .9, 1]
    nas = [.1, .2, .3, .4, .5]
    center = 0
    figname = 'figures/homophily_perception'
    if not baseline_correction:
        cvs.insert(0, 0)
        center = 1
        ylabel = r'$B_{group}$'
    else:
        data_a0 = df[df.cv == 0.].pivot("na", "sa", "bias_a")
        data_b0 = df[df.cv == 0.].pivot("na", "sa", "bias_b")
        figname += '_amplification'
        ylabel = 'Induced ' + r'$B_{group}$'
    len_cv = len(cvs)
    fig, axs = plt.subplots(len_cv, 2, figsize=(6.3, 3 * len_cv), sharey=True, sharex=True)
    for row, cv in enumerate(cvs):
        data_a = df[df.cv == cv].pivot("na", "sa", "bias_a")
        data_b = df[df.cv == cv].pivot("na", "sa", "bias_b")
        if baseline_correction:
            data_a = data_a - data_a0
            data_b = data_b - data_b0
        for na in nas:
            axs[row, 0].plot(data_a.loc[na]) #, label='{}'.format(na))
            axs[row, 1].plot(data_b.loc[na], label='{}'.format(na))

        axs[row, 0].annotate(r'$c=$' + '{}'.format(cv), xy=(.3, 6.5), size='large', \
                ha='right', va='center')
        axs[row, 0].axhline(y=center, c='grey', alpha=.5)
        axs[row, 1].axhline(y=center, c='grey', alpha=.5)
        axs[row, 0].axvline(x=0.5, c='grey', alpha=.5)
        axs[row, 1].axvline(x=0.5, c='grey', alpha=.5)

        axs[row, 0].set_ylabel(ylabel)
        axs[row, 1].legend(loc=0, title=r'$n_a=$', labelspacing=.1)
        if log:
            axs[row, 0].set_yscale('log')
    axs[0, 0].set_title('Minority')
    axs[0, 1].set_title('Majority')
    axs[row, 0].set_xlabel(r'$s_a = s_b$')
    axs[row, 1].set_xlabel(r'$s_a = s_b$')

    fig.tight_layout()
    if log:
        figname += '_log'
    fig.savefig(figname + '.pdf')










