import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def bulletgraph_Multiple(data=None, limits=None, labels1=None,labels2=None,labels3=None,lables4=None ,axis_label=None, title=None,
                size=(5, 3), palette=None, formatter=None, target_color="gray",
                bar_color="black", label_color="black",axarr=None,figarr=None,multiple=None):
    """ Build out a bullet graph image
        Args:
            data = List of labels, measures and targets
            limits = list of range valules
            labels = list of descriptions of the limit ranges
            axis_label = string describing x axis
            title = string title of plot
            size = tuple for plot size
            palette = a seaborn palette
            formatter = matplotlib formatter object for x axis
            target_color = color string for the target line
            bar_color = color string for the small bar
            label_color = color string for the limit label text
        Returns:
            a matplotlib figure
    """
   
    # Determine the max value for adjusting the bar height
    # Dividing by 10 seems to work pretty well
    h = limits[-1] / 10

    # Use the green palette as a sensible default
    if palette is None:
        palette = sns.light_palette("green", len(limits), reverse=False)

    

    # Add each bullet graph bar to a subplot
    for idx, item in enumerate(data):

        # Get the axis from the array of axes returned when the plot is created
        ax = axarr[idx]
        # Formatting to get rid of extra marking clutter
        ax.set_aspect('equal')
        # ax.set_yticklabels([item[0]])
        ax.set_yticks([1])
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        prev_limit = 0
        for idx2, lim in enumerate(limits):
            # Draw the bar
            if labels1[idx2]==labels2[idx2] and labels3[idx2]==labels1[idx2] and labels3[idx2]==labels2[idx2] and lables4[idx2]==labels1[idx2] and lables4[idx2]==labels2[idx2] and lables4[idx2]==labels3[idx2]:
                color='green'
                same=True
            elif labels1[idx2]==labels2[idx2] or  labels3[idx2]==labels1[idx2] or labels3[idx2]==labels2[idx2] or lables4[idx2]==labels1[idx2] or lables4[idx2]==labels2[idx2] or lables4[idx2]==labels3[idx2]:
                color='orange'
                same=False
            else:
                color='red' #mistmatch
            if labels1[idx2]=='-' or labels2[idx2]=='-' or labels3[idx2]=='-' or lables4[idx2]=='-':
                color='white'
            
            ax.barh([1], lim - prev_limit, left=prev_limit, height=h,
                    color=color)
            prev_limit = lim
        rects = ax.patches
        # The last item in the list is the value we're measuring
        # Draw the value we're measuring
        # ax.barh([1], item[1], height=(h / 3), color=bar_color)

        # Need the ymin and max in order to make sure the target marker
        # fits
        ymin, ymax = ax.get_ylim()
        ax.vlines(
            item[2], ymin * .9, ymax * .9, linewidth=1.5, color=target_color)

    # Now make some labels
    if labels1 is not None and labels2 is not None :
        for rect, label, label2, label3, label4  in zip(rects, labels1,labels2, labels3,lables4):
            # if ( label==label2):
            #     color='green'
            # elif label =='_' or label2=="_":
            #     color='yellow'
            # else:
            #     color='red'
            height = rect.get_height()
            axarr[0].text(
                rect.get_x() + rect.get_width() / 1.5,
                -height *.0001,
                label,
                ha='center',
                va='bottom',
                color=label_color)
            axarr[1].text(
            rect.get_x() + rect.get_width() / 1.5,
            -height * .0001,
            label2,
            ha='center',
            va='bottom',
            color=label_color)
            axarr[2].text(
            rect.get_x() + rect.get_width() / 1.5,
            -height * .0001,
            label3,
            ha='center',
            va='bottom',
            color=label_color)
            axarr[3].text(
            rect.get_x() + rect.get_width() / 1.5,
            -height * .0001,
            label4,
            ha='center',
            va='bottom',
            color=label_color)
            
    # if labels2 is not None:
    #     for rect, label in zip(rects, labels2):
    #         height = rect.get_height()
    #         axarr[1].text(
    #             rect.get_x() + rect.get_width() / 1.8,
    #             -height * .1,
    #             label,
    #             ha='center',
    #             va='bottom',
    #             color=label_color)
    if formatter:
        ax.xaxis.set_major_formatter(formatter)
    if axis_label:
        ax.set_xlabel(axis_label)
    if title:
        figarr[0].suptitle(title, fontsize=14)
    figarr[0].subplots_adjust(hspace=0)
    figarr[1].subplots_adjust(hspace=0)

