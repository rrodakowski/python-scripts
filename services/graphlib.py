import os
import logging

import pygal

logger = logging.getLogger(__name__)


class GraphService(object):

    def __init__(self, output_dir):
        logger.debug("Creating the GraphService")
        self.output_dir = output_dir


    def make_bar_chart(self, title, xlabels, statute_values, reg_values, case_values):
        bar_chart = pygal.Bar(legend_at_bottom=True, fill=True) # Then create a bar graph object
        bar_chart.title = title
        bar_chart.x_labels = xlabels
        bar_chart.add('Cases (w_cs_cal1)', case_values)
        bar_chart.add('Statutes (w_codesstacanvdp)', statute_values)
        bar_chart.add('Regulations (w_codesadccanvdp)', reg_values)
        bar_chart.render_to_file(self.output_dir+ os.sep +'bar_chart.svg')

    def make_stacked_bar_chart(self, title, xlabels, statute_values, reg_values, case_values):
        bar_chart = pygal.StackedBar(legend_at_bottom=True, fill=True)
        bar_chart.title = title
        bar_chart.x_labels = xlabels
        bar_chart.add('Cases (w_cs_cal1)', case_values)
        bar_chart.add('Statutes (w_codesstacanvdp)', statute_values)
        bar_chart.add('Regulations (w_codesadccanvdp)', reg_values)
        bar_chart.render_to_file(self.output_dir+ os.sep +'stacked_bar_chart.svg')

    def make_dot_chart(self, title, xlabels, statute_values, reg_values, case_values):
        dot_chart = pygal.Dot(legend_at_bottom=True, x_label_rotation=30)
        dot_chart.title = title
        dot_chart.x_labels = xlabels
        dot_chart.add('Cases (w_cs_cal1)', case_values)
        dot_chart.add('Statutes (w_codesstacanvdp)', statute_values)
        dot_chart.add('Regulations (w_codesadccanvdp)', reg_values)
        dot_chart.render_to_file(self.output_dir+ os.sep +'dot_chart.svg')

    def make_line_chart(self, title, xlabels, statute_values, reg_values, case_values):
        chart = pygal.StackedLine(fill=True, interpolate='cubic')
        chart.title = title
        chart.x_labels = xlabels
        chart.add('Cases (w_cs_cal1)', case_values)
        chart.add('Statutes (w_codesstacanvdp)', statute_values)
        chart.add('Regulations (w_codesadccanvdp)', reg_values)
        chart.render_to_file(self.output_dir+ os.sep +'line_chart.svg')  # Write the chart in the specified file
