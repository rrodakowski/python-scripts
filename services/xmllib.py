import os
import logging
import traceback
import lxml.etree as ET
#import xml.etree.cElementTree as ET
from xml.dom import minidom # used for pretty printing
import services.filelib


logger = logging.getLogger(__name__)


class XmlService(object):

    def __init__(self):
        logger.debug("Creating the XmlService")

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString('<root>'+rough_string+'</root>')
        return reparsed.toprettyxml(indent="\t")

    def find_in_tree(self, tree, node):
        found = tree.find(node)
        if found == None:
            logger.debug("No {} in file").format(node)
            found = []
        return found

    def write_out_to_xml(self, root, output_file):
        #root = ET.Element("root")
        fs = FileService()
        fs.write_raw_text_to_file(output_file, root)

    def evaluate_xpath(self, root, xpath):
        return root.findall(xpath)

    def get_text(self, root):
        for page in list(root):
            title = page.find('title').text
            content = page.find('content').text
            print('title: %s; content: %s' % (title, content))


class TransformService(object):
    """A wrapper for working with XSLT stylesheets"""

    def __init__(self):
        logger.debug("starting the transform service")

    @staticmethod
    def transform_xml_document(xml_filename, xsl_filename, output_dir, output_file, param=None):
        """
        run a xslt stylesheet against a file
        """
        # Parse a xml file (specify the path)
        try:
            logger.info("transforming file {}".format(xml_filename))
            dom = ET.parse(xml_filename)
            xslt = ET.parse(xsl_filename)
            transform = ET.XSLT(xslt)
            newdom = None
            if param is None: # no parameters, just exexute the stylesheet
                logger.info('Transforming with NO paramters')
                newdom = transform(dom)
            else:
                logger.info("Transforming with parameter {}".format(param))
                newdom = transform(dom, param1=ET.XSLT.strparam(param))
            newdom.write(os.path.join(output_dir, output_file))

        except:
            logger.error("Unable to open and parse input file: " + xml_filename)
            traceback.print_exc()

    @staticmethod
    def process_stylesheet_chain(xml_filename, stylesheet_list, output_dir, output_file, remove_temp_files=True, param=None):
        """
        process a chain of stylesheets, set optional remove_temp_files to false
        to keep intermediate output files for use as debugging files.
        """
        logger.info("Transforming xml file {}".format(xml_filename))
        stylesheet_number = 1
        stylesheets_to_process = len(stylesheet_list)
        debug_files = []
        for xsl in stylesheet_list:
            base_xsl = os.path.basename(os.path.splitext(xsl)[0])
            logger.debug("base_xsl is {}".format(base_xsl))
            base_xml = os.path.splitext(os.path.basename(xml_filename))[0]
            logger.debug("base_xml is {}".format(base_xml))
            intermediate_file = os.path.join(output_dir, "{}_{}.xml".format(base_xml, base_xsl))
            logger.debug("intermediate file is {}".format(intermediate_file))
            if stylesheet_number == 1 and stylesheet_number == stylesheets_to_process: # only one stylesheet in chain
                TransformService.process_link(xml_filename, xsl, output_dir, output_file, stylesheet_number, param)
            elif stylesheet_number == 1: # first stylesheet is running
                TransformService.process_link(xml_filename, xsl, output_dir, intermediate_file, stylesheet_number, param)
                debug_files.append(intermediate_file)
                stylesheet_number = stylesheet_number + 1
            elif stylesheet_number < stylesheets_to_process: # a middle stylesheet is running
                TransformService.process_link(debug_files[stylesheet_number-2], xsl, output_dir, intermediate_file, stylesheet_number, param)
                debug_files.append(intermediate_file)
                stylesheet_number = stylesheet_number + 1
            elif stylesheet_number == stylesheets_to_process: # last stylesheet is running
                TransformService.process_link(debug_files[stylesheet_number-2], xsl, output_dir, output_file, stylesheet_number, param)
                logger.info("Finished processing the chain! Output file {} to {}.".format(output_file, output_dir))
                if remove_temp_files:
                    filelib.remove_files(debug_files)

    @staticmethod
    def process_link(xml_filename, xsl, output_dir, output_file, link_number, param=None):
        """
        helper function to process a link (one stylesheet) in a chain of stylesheets
        """
        logger.info('running {} stylesheet as link {} in the chain'.format(xsl, link_number))
        TransformService.transform_xml_document(xml_filename, xsl, output_dir, output_file, param)
