import numpy
import csv


def smoothList(list, strippedXs=False, degree=10):

    if strippedXs==True: return Xs[0: - (len(list) - (len(list) - degree + 1))]

    smoothed = [0] * (len(list) - degree + 1)

    for i in range(len(smoothed)):

        smoothed[i] = sum(list[i:i + degree]) / float(degree)

    return smoothed


def smoothListTriangle(list, strippedXs=False, degree=5):

    weight = []

    window = degree*2-1

    smoothed = [0.0] * (len(list) - window)

    for x in range(1, 2 * degree) : weight.append(degree - abs(degree - x))

    w = numpy.array(weight)

    for i in range(len(smoothed)):

        smoothed[i] = sum(numpy.array(list[i:i + window]) * w) / float(sum(w))

    return smoothed


def smoothListGaussian(list, strippedXs=False, degree=5):

    window = degree * 2 - 1

    weight = numpy.array([1.0] * window)

    weightGauss = []

    for i in range(window):

        i = i - degree + 1

        frac = i / float(window)

        gauss = 1 / (numpy.exp((4 * (frac)) ** 2))

        weightGauss.append(gauss)

    weight = numpy.array(weightGauss) * weight

    smoothed = [0.0] * (len(list) - window)

    for i in range(len(smoothed)):

        smoothed[i] = sum(numpy.array(list[i:i + window]) * weight) / sum(weight)

    return smoothed


def avg(values):
    """ Calculates mean of a list of numbers
    """
    return sum(values) / float(len(values))


def stdev(values):
    """ Calculates standard deviation of a list
    """
    mean = avg(values)

    diffs = [(value - mean) ** 2 for value in values]

    return avg(diffs) ** 0.5


def GetScores(chrom, start, end):
    '''
    need to implement
    '''
    return 1


def GetBounds(l):
    std = numpy.std(l)
    mean = numpy.average(l)

    low = mean - std

    mark1 = -1
    mark2 = -1

    length = len(l)
    for i in range(length):
        if mark1 == -1:
            pt1 = l[i]
            if pt1 < low:
                mark1 = i

        if mark2 == -1:
            pt2 = l[length-i-1]
            if pt2 < low:
                mark2 = length-i-1

        if mark1 != -1 and mark2 != -1:
            break

    return [mark1, mark2]


offset = 2000

filename = '/afs/ir/class/cs173/finalProjects/GREATRegDoms/ontologies/hg18/hg18.loci'
f = open(filename, 'rb')  # used to be gzip.open
lines = list(csv.reader(f, delimiter='\t'))
f.close()

for i in range(len(lines)):
    first = int(lines[i][2])
    second = int(lines[i + 1][2])
    chrom1 = lines[i][1]
    chrom2 = lines[i + 1][1]
    if (chrom1 != chrom2):
        print "Done with " + chrom1
        continue

    start = first
    end = second
    if second - first > 2 * offset:
        start = first + offset
        end = second - offset

    l = GetScores(chrom1, start, end)
    l = smoothListGaussian(l)
    bounds = GetBounds(l)
