def generate_latex_template(name, course, roll, phone, emaila, emailb, github, website, linkedin, education_details, experience_details, project_details):
    return r"""
\documentclass[a4paper,11pt]{article}
\usepackage{latexsym}
\usepackage{xcolor}
\usepackage{float}
\usepackage{ragged2e}
\usepackage[empty]{fullpage}
\usepackage{wrapfig}
\usepackage{lipsum}
\usepackage{tabularx}
\usepackage{titlesec}
\usepackage{geometry}
\usepackage{marvosym}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage{multicol}
\usepackage{graphicx}
\usepackage{cfr-lm}
\usepackage[T1]{fontenc}
\setlength{\multicolsep}{0pt} 
\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\geometry{left=1.4cm, top=0.8cm, right=1.2cm, bottom=1cm}
% Adjust margins
%\addtolength{\oddsidemargin}{-0.5in}
%\addtolength{\evensidemargin}{-0.5in}
%\addtolength{\textwidth}{1in}
\usepackage[most]{tcolorbox}
\tcbset{
	frame code={}
	center title,
	left=0pt,
	right=0pt,
	top=0pt,
	bottom=0pt,
	colback=gray!20,
	colframe=white,
	width=\dimexpr\textwidth\relax,
	enlarge left by=-2mm,
	boxsep=4pt,
	arc=0pt,outer arc=0pt,
}

\urlstyle{same}

\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-7pt}]

%-------------------------
% Custom commands
\newcommand{\resumeItem}[2]{
  \item{
    \textbf{\#1}{:\hspace{0.5mm}\#2 \vspace{-0.5mm}}
  }
}

\newcommand{\resumePOR}[3]{
\vspace{0.5mm}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{\#1},\hspace{0.3mm}\#2 & \textit{\small{\#3}} 
    \end{tabular*}
    \vspace{-2mm}
}

\newcommand{\resumeSubheading}[4]{
\vspace{0.5mm}\item
    \begin{tabular*}{0.98\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{\#1} & \textit{\footnotesize{\#4}} \\
        \textit{\footnotesize{\#3}} &  \footnotesize{\#2}\\
    \end{tabular*}
    \vspace{-2.4mm}
}

\newcommand{\resumeProject}[4]{
\vspace{0.5mm}\item
    \begin{tabular*}{0.98\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{\#1} & \textit{\footnotesize{\#3}} \\
        \footnotesize{\textit{\#2}} & \footnotesize{\#4}
    \end{tabular*}
    \vspace{-2.4mm}
}

\newcommand{\resumeSubItem}[2]{\resumeItem{\#1}{\#2}\vspace{-4pt}}

% \renewcommand{\labelitemii}{$\circ$}
\renewcommand{\labelitemi}{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=*,labelsep=0mm]}
\newcommand{\resumeHeadingSkillStart}{\begin{itemize}[leftmargin=*,itemsep=1.7mm, rightmargin=2ex]}
\newcommand{\resumeItemListStart}{\begin{justify}\begin{itemize}[leftmargin=3ex, rightmargin=2ex, noitemsep,labelsep=1.2mm,itemsep=0mm]\small}

\newcommand{\resumeSubHeadingListEnd}{\end{itemize}\vspace{2mm}}
\newcommand{\resumeHeadingSkillEnd}{\end{itemize}\vspace{-2mm}}
\newcommand{\resumeItemListEnd}{\end{itemize}\end{justify}\vspace{-2mm}}
\newcommand{\cvsection}[1]{%
\vspace{2mm}
\begin{tcolorbox}
    \textbf{\large \#1}
\end{tcolorbox}
    \vspace{-4mm}
}

\newcolumntype{L}{>{\raggedright\arraybackslash}X}%
\newcolumntype{R}{>{\raggedleft\arraybackslash}X}%
\newcolumntype{C}{>{\centering\arraybackslash}X}%
%---- End of Packages and Functions ------

%-------------------------------------------
%%%%%%  CV STARTS HERE  %%%%%%%%%%%
%%%%%% DEFINE ELEMENTS HERE %%%%%%%
\newcommand{\name}{name} % Your Name
\newcommand{\course}{branch} % Your Course
\newcommand{\roll}{roll} % Your Roll No.
\newcommand{\phone}{phone} % Your Phone Number
\newcommand{\email}{email} %Email 1
\newcommand{\github}{github} %Github
\newcommand{\website}{website} %Website
\newcommand{\linkedin}{linked} %linkedin




\begin{document}
\fontfamily{cmr}\selectfont
%----------HEADING-----------------
\parbox{2.35cm}{%

\includegraphics[width=2cm,clip]{iitg_logo.jpg}

}\parbox{\dimexpr\linewidth-2.8cm\relax}{
\begin{tabularx}{\linewidth}{L r}
  \textbf{\LARGE \name} & +91-\phone\\
  {Roll No.:\roll} & \href{mailto:\emaila}{\emaila} \\
  \course &  \href{mailto:\emailb}{\emailb}\\
  {br} &  \href{\github}{Github} $|$ \href{\website}{Website}\\
  {Indian Institute Of Technology, Guwahati} & \href{https://www.linkedin.com/in/\linkedin/}{linkedin.com/in/\linkedin}
\end{tabularx}
}



%-----------EDUCATION-----------------
{% block education %}
{% endblock %}

%-----------EXPERIENCE-----------------
{% block experience %}
{% endblock %}

%-----------PROJECTS-----------------
{% block projects %}
{% endblock %}

%-----------TECHNICAL SKILLS-----------------
{% block technical_skills %}
{% endblock %}

%-----------KEY COURSE PROJECTS-----------------
{% block key_course_projects %}
{% endblock %}

%-----------POSITIONS OF RESPONSIBILITY-----------------
{% block positions_of_responsibility %}
{% endblock %}

%-----------ACHIEVEMENTS-----------------
{% block achievements %}
{% endblock %}


%-------------------------------------------
\end{document}


"""

