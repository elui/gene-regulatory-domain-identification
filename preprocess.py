

output = open('chr1_transcript_phastCons','w')

def file_data(filename):
  filedata = open(filename,'r')
  line = filedata.readline()
  while line:
    line = line.split()
    if len(line) == 1:
      yield line
    else: 
      yield line[2].split('=')
    line = filedata.readline()

     
def read_transcription_starts(filename,chromosome):
  filedata = open(filename,'r').readlines()
  result = []
  for line in filedata:
    line = line.split()
    if line[1] != chromosome:
      return result
    else:
      result.append(int(line[2]))
    

def check_transcription_start(transcriptionStarts,iterIndex,transcriptionIndex):
  transcriptionStartstart = int(transcriptionStarts[transcriptionIndex][0])
  transcriptionEnd = int(transcriptionStarts[transcriptionIndex][1])
  if transcriptionStartstart == iterIndex:
    output.write('start\n')
  if transcriptionStartstart <= iterIndex and transcriptionEnd > iterIndex:
    return True
  else:
    return False


""" Preprocess phastCons chromosomes to break into smaller chunks

"""



if __name__=="__main__":
  chromeFilename = 'phastCons28way/chr1.pp'
  transcriptionStartFilename = 'GREATRegDoms/ontologies/hg18/hg18.loci'
  phastFiledata = file_data(chromeFilename)
  transcriptionStarts = read_transcription_starts(transcriptionStartFilename,'chr1')

  iterIndex = 0
  start = transcriptionStarts[0]
  transcriptionIndex = 1
  numStartSites = len(transcriptionStarts)
  output_prefix = 'phastcons28way-chr1-'
  suffix = 0
  

  for i in range(start):
    phastFiledata.next()
    iterIndex += 1
  for line in phastFiledata:
    if iterIndex % 1000000 == 0:
      output.close()
      output = open(output_prefix+str(suffix),'w')
      output.write('start\n')
      suffix += 1
    if iterIndex % 1000000 == 0:
      print "transcriptionIndex: %d" %(transcriptionIndex)
      print iterIndex
    if len(line) > 1:
      phastStart = int(line[1])
      for j in range(iterIndex,phastStart):
        score = 0
        if iterIndex < transcriptionStarts[transcriptionIndex]:
          output.write(str(score)+'\n')
        else:
          output.write('start\n')
          transcriptionIndex += 1
        
        iterIndex += 1
    else:
      score = float(line[0])
      if iterIndex < transcriptionStarts[transcriptionIndex]:
        output.write(str(score)+'\n')
      else:
        output.write('start\n')
        transcriptionIndex += 1
      iterIndex += 1
      
      





