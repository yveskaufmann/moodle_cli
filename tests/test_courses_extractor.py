import pytest

from bs4 import BeautifulSoup
from moodle_cli.extractors import CoursesExtractor

class TestCoursesExtractor:

	@pytest.mark.parametrize("empty_input", ['', None])
	def test_extract_from_empty_markup(self, empty_input):
		extractor = CoursesExtractor(empty_input)
		result = extractor.extract()
		assert isinstance(result, list)
		assert len(result) == 0

	@pytest.mark.parametrize("markup, expeted_semester", [
		("""<div class="termdiv coc-term-2016-1 coc-hidden"></div> """, "2016-1"),
		("""<div class="coc-term-2015-2"></div>""", "2015-2"),
		("""<div class="blu blu blu"></div>""", "")
	])
	def test_extract_semester_from_class(self, markup, expeted_semester):
		extractor = CoursesExtractor(markup)
		semester = extractor._extract_semester_from_class(extractor.parser.div)

		assert semester == expeted_semester

	def test_extract_courses(self):

		coures_markup = """
		<div class="content">
		<div id="coc-courselist" class="row-fluid">
		<div id="coc-course-8436" class="coc-course">
			<div class="termdiv coc-term-2015-2 coc-hidden">
			<div class="teacherdiv coc-teacher-836">
				<div class="box coursebox">
					<div class="hidecourseicon">
						<a href="https://moodle.htw-berlin.de/my/index.php?coc-manage=0&amp;coc-hidecourse=8436&amp;coc-showcourse"
							id="coc-hidecourse-8436" title="Kurs verbergen">
							<img src="https://moodle.htw-berlin.de/theme/image.php/htw/core/1474719679/t/hide"
							class="icon" alt="Kurs verbergen">
						</a>
						<a href="https://moodle.htw-berlin.de/my/index.php?coc-manage=0&amp;coc-hidecourse&amp;coc-showcourse=8436"
							id="coc-showcourse-8436" class="coc-hidden" title="Kurs anzeigen">
							<img src="https://moodle.htw-berlin.de/theme/image.php/htw/core/1474719679/t/show"
							class="icon" alt="Kurs anzeigen">
						</a>
					</div>
					<h3>
						<a title="AWE: Virtuelle Klangwelten Za WiSe2015" href="https://moodle.htw-berlin.de/course/view.php?id=8436">
							AWE: Virtuelle Klangwelten Za WiSe2015<br>
							<span class="coc-metainfo">(AWE VIRTKW-109758-Za  |  Sascha Baumeister)</span>
						</a>
					</h3>
				</div>
			</div>
			</div>

			<div id="coc-course-11133" class="coc-course">
			<div class="termdiv coc-term-2016-2">
				<div class="teacherdiv coc-teacher-4662">
					<div class="box coursebox">
						<div class="hidecourseicon">
							<a href="https://moodle.htw-berlin.de/my/index.php?coc-manage=0&amp;coc-hidecourse=11133&amp;coc-showcourse"
							id="coc-hidecourse-11133" title="Kurs verbergen">
							<img src="https://moodle.htw-berlin.de/theme/image.php/htw/core/1474719679/t/hide"
								class="icon" alt="Kurs verbergen">
							</a>
							<a href="https://moodle.htw-berlin.de/my/index.php?coc-manage=0&amp;coc-hidecourse&amp;coc-showcourse=11133"
							id="coc-showcourse-11133" class="coc-hidden" title="Kurs anzeigen">
								<img src="https://moodle.htw-berlin.de/theme/image.php/htw/core/1474719679/t/show"
								class="icon" alt="Kurs anzeigen">
							</a>
						</div>
						<h3>
							<a title="AWE Wissenschaftliches Arbeiten mit LaTeX  WiSe2016"
							href="https://moodle.htw-berlin.de/course/view.php?id=11133">
							AWE Wissenschaftliches Arbeiten mit LaTeX  WiSe2016<br>
								<span class="coc-metainfo">(AWE-WiArLa-116274-  |  Sophie Kröger)</span>
							</a>
						</h3>
					</div>
				</div>
			</div>
			</div>

		</div>
		</div>
		</div>
		"""
		extractor = CoursesExtractor(coures_markup)
		result = extractor.extract()

		assert isinstance(result, list) and len(result) == 2
		assert isinstance(result[0], dict) and isinstance(result[1], dict)

		assert result[0]['title'] == 'AWE: Virtuelle Klangwelten Za WiSe2015'
		assert result[0]['dozent'] == 'Sascha Baumeister'
		assert result[0]['cousre_url'] == 'https://moodle.htw-berlin.de/course/view.php?id=8436'
		assert result[0]['semester'] == '2015-2'

		assert result[1]['title'] == 'AWE Wissenschaftliches Arbeiten mit LaTeX  WiSe2016'
		assert result[1]['dozent'] == 'Sophie Kröger'
		assert result[1]['cousre_url'] == 'https://moodle.htw-berlin.de/course/view.php?id=11133'
		assert result[1]['semester'] == '2016-2'





