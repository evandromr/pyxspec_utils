# coding: utf-8
""" Manipulate python data to produce Xspec readable files"""
from astropy.io import fits
import numpy as np
import os


def read_from_txt(filename):
    """Reads a text file to create xspec readable fits file

    Parameters
    ----------
    filename: str
        A text files with 2 or 3 columns to read.

    Returns
    -------
    energies, values(, erros): ndarrays
        The columns present in the file text

    Raises
    ------
    IOError
        If the files has less than 2 or more than 3 columns or is read as such
        due to formatting.
    """

    table = np.loadtxt(filename).T

    if table.shape[0] == 2:
        energies = table[0]
        yvalues = table[1]
        return energies, yvalues
    elif table.shape[0] == 3:
        energies = table[0]
        yvalues = table[1]
        yerrors = table[2]
        return energies, yvalues, yerrors
    else:
        raise IOError("File has {} columns".format(table.shape[0]))


def fake_pha(values, energies,
             errors=None,
             prefix="fake",
             respfile="NONE",
             telescope="FAKE", instrument="FAKE",
             afilter="NONE", backfile="NONE",
             corrfile="NONE", ancrfile="NONE",
             syserr=0, date="2001-01-01"):
    """ Creates a fake pha file to be read fitted with xspec

        Parameters
        ----------
        values: ndarray
            Values of the fake data
        energies: ndarray
            Array of bin edges for the x-axis (lenght of values + 1)
        errors: ndarray, optional
            statistical error of the fake data. Default is zero
        prefix: str, optional
            A prefix to save file as <prefix>.pha. Defauls is "fake"

        Other Parameters
        ----------------
        date: str
            File creation date. Default is "2001-01-01"
        telescope: str
            Name of the mission/telescope
        instrument: str
            Name of the instrument used
        afilter: str
            FILTER keyword
        respfile: str
            Response file.
        backfile: str
            Background file
        corrfile: str
            CORRFILE keyword
        ancrfile: str
            ANCRFILE keyword
        syserr: float
            systematic error on data

        Returns
        -------
        Creates <prefix>.pha file in the current directory
    """

    hdu1 = fits.PrimaryHDU()

    hdu1.header["DATE"] = date, "Fake creation date"
    hdu1.header["TELESCOP"] = telescope, "Fake mission name"
    hdu1.header["INSTRUME"] = instrument, "Fake instrument name"
    hdu1.header["CONTENT"] = "SPECTRUM"
    hdu1.header["PHAVERSN"] = "1992a"

    if errors is None:
        errors = np.zeros_like(values)

    counts = np.array([val*(energies[i+1]-energies[i]) for i,val in enumerate(values)])
    stat_err = np.array([err*(energies[i+1]-energies[i]) for i,err in enumerate(errors)])
    channels = np.arange(1, len(energies))

    col_channel = fits.Column(name="CHANNEL", format="1I", array=channels)
    col_counts = fits.Column(name="COUNTS", format="1D", array=counts)
    col_stat_err = fits.Column(name="STAT_ERR", format="1D", array=stat_err)
    pha_cols = fits.ColDefs([col_channel, col_counts, col_stat_err])

    pha_head = fits.Header()
    pha_head["EXTNAME"] = "SPECTRUM"
    pha_head["TELESCOP"] = telescope
    pha_head["INSTRUME"] = instrument
    pha_head["FILTER"] = afilter
    pha_head["EXPOSURE"] = 1.0
    pha_head["AREASCAL"] = 1.0
    pha_head["BACKSCAL"] = 1.0
    pha_head["CORRSCAL"] = 1.0
    pha_head["BACKFILE"] = backfile
    pha_head["CORRFILE"] = corrfile
    pha_head["RESPFILE"] = respfile
    pha_head["ANCRFILE"] = ancrfile
    pha_head["POISSERR"] = False
    pha_head["CHANTYPE"] = "PHA"
    pha_head["DETCHANS"] = len(channels)
    pha_head["SYS_ERR"] = syserr
    pha_head["QUALITY"] = 0
    pha_head["GROUPING"] = 0
    pha_head["HDUCLASS"] = "OGIP"
    pha_head["HDUCLAS1"] = "SPECTRUM"
    pha_head["HDUVERS"] = "1.1.0"

    spechdu = fits.BinTableHDU.from_columns(pha_cols, header=pha_head)
    phafile = fits.HDUList([hdu1, spechdu])
    phafile.writeto("{}.pha".format(prefix), overwrite=True)


def fake_rmf(energies, prefix="fake",
             telescope="FAKE", instrument="FAKE",
             date="2001-01-01", afilter="NONE",
             effarea=1.0):
    """ Creates a dummy rmf file with a diagonal response

        Parameters
        ----------
        energies: ndarray
            Array of bin edges for the x-axis (lenght of values + 1)
        prefix: str, optional
                A prefix to save file as <prefix>.pha. Defauls is "fake"

        Other Parameters
        ----------------
        date: str
            File creation date. Default is "2001-01-01"
        telescope: str
            Name of the mission/telescope
        instrument: str
            Name of the instrument used
        afilter: str
            FILTER keyword
        effarea: float
            EFFAREA keyword.

        Returns
        -------
        Creates <prefix>.rmf file in the current directory
    """
    prihdu = fits.PrimaryHDU()

    prihdu.header["DATE"] = date, "Fake creation date"
    prihdu.header["TELESCOP"] = telescope, "Fake mission name"
    prihdu.header["INSTRUME"] = instrument, "Fake instrument name"
    prihdu.header["CONTENT"] = "SPECTRUM"

    channels = np.arange(len(energies) - 1)

    energ_lo = np.array(energies[:-1])
    energ_hi = np.array(energies[1:])
    n_grp = np.ones_like(channels)
    f_chan = np.ones_like(channels)
    n_chan = np.full_like(channels, len(channels))

    matrix = []
    identi = np.identity(len(channels))
    for row in identi:
        matrix.append(np.array(identi))
    matrix = np.asarray(matrix)

    col_energ_lo = fits.Column(name="ENERG_LO", format="1D",
                               array=energ_lo, unit="keV")
    col_energ_hi = fits.Column(name="ENERG_HI", format="1D",
                               array=energ_hi, unit="keV")
    col_n_grp = fits.Column(name="N_GRP", format="1I", array=n_grp)
    col_f_chan = fits.Column(name="F_CHAN", format="1I", array=f_chan)
    col_n_chan = fits.Column(name="N_CHAN", format="1I", array=n_chan)
    col_matrix = fits.Column(name="MATRIX", format="{}E".format(len(channels)),
                             array=identi)

    matrix_cols = fits.ColDefs([col_energ_lo,
                                col_energ_hi,
                                col_n_grp,
                                col_f_chan,
                                col_n_chan,
                                col_matrix])

    m_head = fits.Header()
    m_head["EXTNAME"] = "MATRIX", "name of this binary table extension"
    m_head["TELESCOP"] = telescope, "Fake Mission name"
    m_head["INSTRUME"] = instrument, "Fake instrument name"
    m_head["FILTER"] = afilter
    m_head["CHANTYPE"] = "PHA"
    m_head["DETCHANS"] = len(channels)
    m_head["LO_THRES"] = 0
    m_head["EFFAREA"] = effarea
    m_head["RMFVERSN"] = "1992a"
    m_head["DATE"] = date, "Fake production date"
    matrixhdu = fits.BinTableHDU.from_columns(matrix_cols, header=m_head)

    col_emin = fits.Column(name="E_MIN", format="1D", array=energ_lo,
                           unit="keV")
    col_emax = fits.Column(name="E_MAX", format="1D", array=energ_hi,
                           unit="keV")
    col_channel = fits.Column(name="CHANNEL", format="1J", array=channels)
    bound_cols = fits.ColDefs([col_emin,
                               col_emax,
                               col_channel])
    head2 = fits.Header()
    head2["EXTNAME"] = "EBOUNDS", "name of this binary table extension"
    head2["FILTER"] = afilter
    head2["CHANTYPE"] = "PHA"
    head2["EFFAREA"] = effarea
    head2["RMFVERSN"] = "1992a"
    head2["DATE"] = date, "Fake production date"
    boundshdu = fits.BinTableHDU.from_columns(bound_cols, header=head2)

    rmffile = fits.HDUList([prihdu, matrixhdu, boundshdu])
    rmffile.writeto("{}.rmf".format(prefix), overwrite=True)
