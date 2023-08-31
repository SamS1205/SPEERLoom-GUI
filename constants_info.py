#Terminology Definitions
warp_def = "These threads run lengthwise (vertically) through the cloth. The loom holds these threads under tension\
\nwhile weaving."
weft_def = "These threads run side to side (horizontally) in the cloth. The weft thread is inserted or thrown by the weaver."

weft_face_def = "Weft-faced weaving is defined as the weft-yarn being the only visible thread in the final fabric once woven.\
\nIn general to achieve weft-faced weaving, choose a warp thread much smaller with less weight\
\nthan the weft yarn."
warp_face_def = "Warp-faced weaving is defined as the warp-yarn being the only visible thread in the final fabric once woven.\
\nIn general to achieve warp-faced weaving, choose a weft thread(s) much smaller with less weight\
\nthan the warp yarn."
balance_weave_def="A balanced-weave denotes a type of weaving structure where the warp and weft threads share\
\nsimilar physical properties such as size, weight, elasticity, and material."

heddle_def  = "Heddles select the threads the loom raises or lowers to make an opening (shed) for the shuttle (pick) to \
\npass through. In shaft loom weaving, heddles are connected to the shaft to easily raise groups of threads for\
\nmore complex patterns. In contrast, a Jacquard loom actuates every heddle individually."
shaft_def   = "Shafts are long rods connected to warp threads through the heddles to raise or lower threads."
shed_def    = "The opening created in the warp when threads are raised or lowered by the heddle."
shuttle_def = "A tool designed to hold and store the weft thread, thrown through the shed while weaving."
float_def   = "When one thread passes over multiple other threads, we call this jump a float because the given thread \
\n \"floats\" on top of the others. Floats allow for weaving structures to be more fluid or flexible.\n"

#Weaving Draft Legend Definitions
threading_def = "The threading is the horizontal grid at the top of the draft. Each row represents a shaft,\
\nwith the one on the bottom representing the shaft closest to you (shaft #1), and the one on the top,\
\n(shaft #4) the farthest. The columns in the threading draft represent a single thread."

tie_up_def    = "The tie-up is represented by the small square at the upper right of your weaving draft.\
\nThe tie-up is the connection point between your threading draft and the pedals (treadles) you operate while weaving.\
\nThe rows represent the shafts (just like the threading!), and the columns represent your treadles.\
\nWhen you press a treadle, the tie-up tells the loom which shafts rise and which shafts fall \n(depending on the type of loom you have)."

treadling_def = "The treadling, referred to as the pedaling by some, is the grid that travels vertically\
\nbelow the tie-up. The treadling is the instructions that you\'ll follow when sitting at your loom: \
\neach row represents one pick of weft/one throw of your shuttle, \
\nwhile each column represents a treadle. It is read from the top (closest to the tie-up) down."

drawdown_def = "This is a visual representation of what happens when you are weaving. \
\nIt is positioned under the threading draft and to the left of the treadling. \
\nIt shows what each warp and weft thread is doing during each pick."

#Simple Pattern Definitions
cp_info = "We will describe and provide examples of the 3 major basic weaving structures: plain, twill, and satin.\
\nAdditionally, we will highlight two more complex culturally important weaving structures, such as\
\nthe West African kente cloth and traditional Mayan huipil dress."

plain_weave_def= "The plain weave is the simplist of all weaving structures.\
\nThis structure consist of equally alternativing the warp & weft threads to create an interlocking pattern."

twill_weave_def= "The twill weave is the second univerally recognized basic weaving structure.\
\nThis structure is denoted with the notation (U x O) twill, where the weft thread \
\npassing under U warp threads then over O warp threads.\
\nPlease note the example above depicts a 2x2 twill weave."

satin_weave_def= "The satin weave is the final major basic weaving structure. The satin weave denotes four or more \
\n warp threads passing over or floating above a weft thread. Similar to the twill weave, \
\nthis structure can be denoted by (U x O) satin. Please note the example above depicts\
\na 4x1 weft-facing satin weave."

satin_weave_cul="The origins of the satin weave date back to medivial China. However, some scholars contend silk and\
\nsatin weaving techniques predate 4000 to 3000 B.C. in mainland China. Historically, satin weaving was performed\
\nexclusively with silk, exported along the Silk Road, from the port city of Quanzhou, and worn by the emperor or\
\nhigh-ranking nobility. Now this timeless technique can be enjoyed by people from all walks of life.\n\n"

#Linear Algebra Review Definition
linAlg_info = "We will provide a basic overview of the linear algebra concepts needed to understand the math behind weaving.\
\nThis review will briefly discuss vectors, vector notation, along with vector and matrix operations."

vector_def= "In the simpliest form, vectors are a pair, or set, of numbers/symbols that represent a value or set of values.\
\nThese values can be purely abstract or relate to any user defined data such as a set of geometric coordinates\
\nor linear equations. Vectors are singular in dimension, defined with either one row with multiple columns \
\nor one column with multiple rows.\
\nTraditionally, vectors are denoted in row column format. This means we classify a vector's size or dimension \
\nby the number of rows present, r, and the number of columns, c, shown below."

vector_ops_add= "Vector addition consists of adding the corresponding elements within each vector.\
\nWe identify corresponding elements by matching these subitems based on their respective position in the\
\noverall vector. Please note you cannot mathematically add vectors of differing sizes or dimensions."

vector_ops_scalar= "Scalar multiplication denotes multiplying the entire vector by a singular constant value.\
\nTo perform scalar multiplication, multiply every single element in the vector with the defined constant."

matrix_def="We define a matrix as a rectangular array of numbers, denoted by any symbol such as A. Similarly, \
\na matrix can be defined as a collection of vectors. Similar to vectors, matracies sizes are defined \
\nin row column format. For example, when A has m rows and n columns, it is an \"m by n\" matrix. \
\nWe will use matracies to convert the separate components of the weaving draft into solvable mathematic\n operations."

matrix_ops="The rules for matrix operations follow closely with those of vector operations.\
\n1. Matracies can only be added if their shapes are the same.\
\n2. They can be multiplied by any scalar value.\
\n3. To multiply two matracies A*B, traditionally written as AB: If A has n columns, B must have n rows.\
\na. The entry in row i and column j of AB is (row i of A) * (column j of B)\
\n\nExample:"

#Cultural Definitions
kente_def = "The kente cloth is a complex woven structure orginating from West Africa. In order to weave a single square\
\npattern (shown below), please follow the provided weaving draft."
kente_instruct= "Please note this structure requires multiple yarn colors for both the warp and weft threads.\
\nSpecifically, the example requires red, green, and yellow yarn for the warp threads along with\
\nseparate black and yellow weft threads, indicated by the colored row and column, respectively.\
\nWe recommend a balance weave for this structure, relying on yarns with similar physical properties will\
\nresult in the most distinct woven pattern."

kente_cult="The kente cloth originates from the nation of Ghana off the coast of West Africa, stemming from the\
\nAsante people during the seventeenth century. Traditionally, masculine-identifying individuals wore\
\nthese garments over their shoulder whereas women-identifying individuals wore these clothes as two\
\nseparate peices, one as an ankle-length dress along with a sling to carry supplies or a child.\
\nEvery aspect of the cloth communicates a message about the wearer through the colors:\
\nGold = Status/Serenity\nYellow = Fertility\nGreen = Renewal\nBlue = Pure Spirit/Harmony\nRed = Passion\nBlack = Spiritual Awareness\
\n\nThese colors and patterns convey common motifs that reflect Asante worldviews such as\
\nNkum me fie na nkosu me aboten, translating to \"Don\'t Kill my house and then mourn\
\nfor me in public\" which warns against untrustworthly people."
kente_cult_2="In modern day, African-American students dawn the kente cloth for collegiate graduation ceremonies.\
\nThis practice originiates the fist prime minister of independent Ghana, Kwame Nkrumah, who wore\
\na kente when meeting President Eisenhower at the White House in 1958.\n\n"

mayan_def="The Mayan people have numerous unique weaving patterns, conveying the wearer's social\
\nstatus and hertitage. These patterns draw inspiration from nature and the natural environment.\
\nTypically, patterns will combine depictions of seeds, animals, flowers, or land formations specific\
\nto the community's region. We will focus on the a traditional huipil design of the San Antonio Aguas\
\nCaliente people in Guatemala, currently stored at the Minneapolis Institute of Art."
mayan_cult="The huipil is a traditional Mayan dress created from a rectangular woven textile whose ends are folded\
\nand sewed together vertically, leaving space for the arms and cut-out for the head. In general, huipils\
\nconsist of red and white cloth. However, every group of Mayan people has a different style and pattern\
\nfor their respective community. These Mayan communities originate from the northwestern part of the\
\nisthmus of Central America, modern day Southern Mexico, extending through Guatemala, Honduras, Belize,\
\nEl Savador, and Nicaragua."

mayan_instruct= " In order to weave a single square pattern (shown above), please follow the provided weaving\
\ndraft. Please note this is a 7-shaft 7-pedal structure, requiring green warp and red weft threads, respectively.\
\nAgain, this thread orientation is indicated by the colored row and column, respectively.\
\nThe treadling for this draft depicts multiple pedal presses at a singular timestep, uncommon in traditional\
\nweaving. However, this constraint does not apply to our machine as the pedal presses are virtual by nature.\
\nWe strongly recommend a balance weave for this structure to achieve the best final results."

mayan_cult_2 ="We recognize this knowledge of traditional Mayan weaving patterns has been pass down through\
\nthe generations of women in these communities, opposing the historical narrative that these styles\
\narose during Spanish colonization in the 1500s."

mathMode_instruct="Let's get ready to explore the math behind our weaving structures!\
\nIn this mode, you will be able to freely manipulate the standard matracies in a weaving draft to\
\nobserve their effecct on th final woven pattern.\
\n_________________________________________________________"

mathMode_instruct_2="\
\n1. In math mode, practice matrix multiplication by configuring the matrices that are multiplied together, \
\n      referred to as the factors or factor matrices.\
\n2. Next, calculate the result of the multiplication operation and configure the resultant or Product (P) matrix.\
\n3. Finally, check your answer with button located in the top right corner!"

mathMode_instruct_3="Note: Do not worry if you compute the wrong answer! The system will highlight the incorrect positions in the matrix for you to focus in on.\n"

mathMode_instruct_4="\nThe diagram above highlights the overall matrix multiplication between the Treadling (Tr), Tie-upᵀ (Tuᵀ), \
\nand Threading (Th) matracies, respectively. The next page of math mode will specifically focus on the multiplication between \
\nthe Threading (Th) and Tie-upᵀ (Tuᵀ) matracies, resulting in a Product (P) matrix. The second page will highlight the multiplication\
\nbetween this Product (P) matrix and the Treadling (Tr) to compute the Drawdown (D) matrix.\n"