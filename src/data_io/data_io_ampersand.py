import os, re
from bs4 import BeautifulSoup

class DataIOAmpersand():

    def clean_text(self, text):
                   
        text = text.strip(' _\t\n')
        text = text.split('____')[0]                                                    #To remove footnotes
        text = text.strip(' _\t\n')
        text = re.sub(r'\(https?://\S+\)', '<url>', text)                               #To remove URLs
        text = re.sub(r'&gt;.*(?!(\n+))$', '', text)                                    #To remove quotes at last.
        text = re.sub(r'\n', ' ', text)
        text = text.rstrip(' _\n\t')
        text = re.sub(r'\n', ' ', text)
        text = text.lower()
        for elem in ['.', ',', ':', '!', ';', '*', '\"', '\'', '(', ')', '[', ']', '<url>', '?','-']:
            text = text.replace(elem, ' '+elem+' ')
        return text

    def file_loader(self, folder):
        """
        Each file that is loaded is returned as 
        a string of all the xml data inside it.
        """
        for f in os.listdir(folder):
            filename = os.path.join(folder, f)
            if os.path.isfile(filename) and filename.endswith('.xml'):
                with open(filename, 'r') as g:
                    yield g.read()

    def refine_xml(self, xml_string):
        xml_string = re.sub(r'<claim [^>]*>', r'<claim>', xml_string)
        xml_string = re.sub(r'<premise [^>]*>', r'<premise>', xml_string)
        return xml_string

    def divide_pc(self, post):
        """
        Divides a post/comment into various contiguous parts 
        corresponding to claims/premises
        """
        type_lis = []
        str_lis = []

        for elem in post:

            s = self.clean_text( str(elem) )
            if s=='':
                continue
            if s.startswith('<claim>'):
                str_lis.append( s[7:-8] )
                type_lis += ['B-C']+['C-C']*(len(str_lis[-1].split(' '))-1)
            elif s.startswith('<premise>'):
                str_lis.append( s[9:-10]  )
                type_lis += ['B-P']+['C-P']*(len(str_lis[-1].split(' '))-1)
            else:
                str_lis.append( s )
                type_lis += ['O']*len(str_lis[-1].split(' '))

        return str_lis, type_lis        

    def thread_generator(self, folder):
        thread_wise_words = []
        thread_wise_tags = []
        
        for xml_string in self.file_loader(folder):
            thread, authors, i = [], {}, 0
            xml_string = self.refine_xml(xml_string)
            parsed_xml = BeautifulSoup(xml_string, "xml")
            
            for elem in parsed_xml.find_all('reply')+[parsed_xml.find('OP')]:
                thread.append( self.divide_pc(elem.contents) )
                
            words_lis = []
            tags_lis = []
            for (str_lis, type_lis) in thread:
                words_lis += (' '.join(str_lis)).split(' ')
                tags_lis += type_lis
            
            thread_wise_words.append(words_lis)
            thread_wise_tags.append(tags_lis)
        
        return thread_wise_words, thread_wise_tags
    
    def read_train_dev_test(self, args):
        word_sequences_train, tag_sequences_train = self.thread_generator(args.train)
        word_sequences_dev, tag_sequences_dev = self.thread_generator(args.dev)
        word_sequences_test, tag_sequences_test = self.thread_generator(args.test)
        
        return word_sequences_train, tag_sequences_train, word_sequences_dev, tag_sequences_dev, word_sequences_test, \
               tag_sequences_test
