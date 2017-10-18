import json
import simplejson
from datetime import datetime, date, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from obsequiemos.forms import UserForm, UserProfileForm, GiftForm, CommentForm, PostForm, PictureForm, PostulationForm, \
    EvaluationForm
from obsequiemos.models import UserProfile, Gift, Comment, Post, Picture, PostStateType, DispatchMethod, CategoryGift, \
    SubcategoryGift, GiftDimensionType, GiftStateType, RegionPost, ProvinciaPost, ComunaPost, Postulations, UserType, \
    UsedTimeType, GiftWeightType, Notifications


def index(request):
    try:
        categories = CategoryGift.objects.all()
        subcategories = SubcategoryGift.objects.all()

        posts = Post.objects.filter(state=True)  # todos los post postulables
        posts_count = posts.count()  # cant de post para postular
        realized_posts = Post.objects.filter(state=False)  # cant de post finalizados
        realized_posts_count = realized_posts.count()
        posts = posts.order_by('-id')[:10]  # 1ros 10 post para postular

        enddate = date.today()
        startdate = enddate - timedelta(days=7)
        last_week_post = Post.objects.filter(date__range=[startdate, enddate]).filter(state=False)
        count_last_week_post = last_week_post.count()
        tomorrow = date.today() + timedelta(days=1)
        today = date.today()

    except Post.DoesNotExist:
        pass

    return render(request, 'index.html', {'posts': posts,
                                          'posts_count': posts_count,
                                          'realized_posts_count': realized_posts_count,
                                          'count_last_week_post': count_last_week_post,
                                          'tomorrow': tomorrow,
                                          'today': today,
                                          'categories': categories,
                                          'subcategories': subcategories,
                                          })


def post(request, post_id):
    data = Post.objects.get(id=post_id)
    user_visit = request.user

    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    if data:

        post = data
        postulations = Postulations.objects.select_related('post_postulation').filter(post_postulation=post)
        count_postulations = postulations.count()
        postulation_winner = postulations.filter(winner=True)
        postulations_selected = Postulations.objects.select_related('post_postulation').all().filter(
            post_postulation=post,
            selected=True)
        success_posts = Post.objects.filter(id=post_id,
                                            state=False)
        count_success_posts = success_posts.count()

        if user_visit:
            postulation_request_user = Postulations.objects.select_related('post_postulation').filter(
                user_postulation=user_visit.id,
                post_postulation=post)

        list_postulation_selected = list(postulations_selected)

        if post.finish_date <= datetime.now().date():
            finish_date = True
        else:
            finish_date = False

        if request.method == 'POST':
            postulation_form = PostulationForm(data=request.POST)
            if postulation_form.is_valid():
                postulation = postulation_form.save(commit=False)
                postulation.user_postulation = request.user
                postulation.post_postulation = post
                postulation.save()
            else:
                print postulation_form.errors
        else:
            postulation_form = PostulationForm()

        return render(request, 'post.html', {'post': post,
                                             'user_visit': user_visit,
                                             'finish_date': finish_date,
                                             'postulations': postulations,
                                             'postulation_form': postulation_form,
                                             'count_postulations': count_postulations,
                                             'postulation_winner': postulation_winner,
                                             'list_postulation_selected': list_postulation_selected,
                                             'count_success_posts': count_success_posts,
                                             'postulation_request_user': postulation_request_user,
                                             'categories': categories,
                                             'subcategories': subcategories,
                                             })
    else:
        return index(request)


# buscador
def post_coincidentes(request):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    # Metodo get, con el que buscan
    if request.method == 'GET':
        busq = request.GET['busqueda']  # string ingresado
        gift_form = GiftForm()
        post_form = PostForm()

        posts = Post.objects.filter(state=True).filter(Q(gift__name__icontains=busq) |
                                                       Q(gift__category__name_category__icontains=busq) |
                                                       Q(gift__subcategory__name_subcategory__icontains=busq) |
                                                       Q(title__icontains=busq)
                                                       )
        posts_count = posts.count()

        return render(request, 'post_coincidentes.html',
                      {'posts': posts,
                       'posts_count': posts_count,
                       'gift_form': gift_form,
                       'post_form': post_form,
                       'busq': busq,
                       'categories': categories,
                       'subcategories': subcategories,
                       })

    if request.method == 'POST':
        busq = request.GET['busqueda']
        if busq == None:
            gifts = None
        region = request.POST.get('region')
        provincia = request.POST.get('provincia')
        comuna = request.POST.get('comuna')
        categoria = request.POST.get('category')
        subcategoria = request.POST.get('subcategory')

        if not region == '---------' and region != None:
            if not provincia == '---------':
                if not comuna == '---------':
                    posts = Post.objects.filter(state=True).filter((Q(gift__name__icontains=busq) |
                                                                    Q(gift__category__name_category__icontains=busq) |
                                                                    Q(
                                                                        gift__subcategory__name_subcategory__icontains=busq) |
                                                                    Q(title__icontains=busq)) &
                                                                   (Q(region__region_name=region) &
                                                                    Q(provincia__provincia_name=provincia) &
                                                                    Q(comuna__id=comuna))
                                                                   )
                else:
                    posts = Post.objects.filter(state=True).filter((Q(gift__name__icontains=busq) |
                                                                    Q(gift__category__name_category__icontains=busq) |
                                                                    Q(
                                                                        gift__subcategory__name_subcategory__icontains=busq) |
                                                                    Q(title__icontains=busq)) &
                                                                   (Q(region__region_name=region) &
                                                                    Q(provincia__provincia_name=provincia))
                                                                   )
            else:
                posts = Post.objects.filter(state=True).filter((Q(gift__name__icontains=busq) |
                                                                Q(gift__category__name_category__icontains=busq) |
                                                                Q(gift__subcategory__name_subcategory__icontains=busq) |
                                                                Q(title__icontains=busq)) &
                                                               (Q(region__region_name=region))
                                                               )
        else:
            if not categoria == '---------' and categoria != None:
                if not subcategoria == '---------' and subcategoria != None:
                    posts = Post.objects.filter(state=True).filter((Q(gift__name__icontains=busq) |
                                                                    Q(gift__category__name_category__icontains=busq) |
                                                                    Q(
                                                                        gift__subcategory__name_subcategory__icontains=busq) |
                                                                    Q(title__icontains=busq)) &
                                                                   (Q(category__name_category=categoria) &
                                                                    Q(subcategory__id=subcategoria))
                                                                   )
                else:
                    posts = Post.objects.filter(state=True).filter((Q(gift__name__icontains=busq) |
                                                                    Q(gift__category__name_category__icontains=busq) |
                                                                    Q(
                                                                        gift__subcategory__name_subcategory__icontains=busq) |
                                                                    Q(title__icontains=busq)) &
                                                                   (Q(category__name_category=categoria))
                                                                   )
            else:
                posts = Post.objects.filter(state=True).filter(Q(gift__name__icontains=busq) |
                                                               Q(gift__category__name_category__icontains=busq) |
                                                               Q(gift__subcategory__name_subcategory__icontains=busq) |
                                                               Q(title__icontains=busq)
                                                               )

        posts_count = posts.count()

        post_form = PostForm(data=None)
        gift_form = GiftForm(data=None)

        return render(request, 'post_coincidentes.html', {'posts': posts,
                                                          'posts_count': posts_count,
                                                          'post_form': post_form,
                                                          'gift_form': gift_form,
                                                          'categories': categories,
                                                          'subcategories': subcategories,
                                                          })

def ingreso(request):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Tu cuenta no esta disponible.')
        else:
            print "Login invalido, ver detalles: {0}, {1}".format(username, password)
            return HttpResponseRedirect('/ingreso/')
    else:
        return render(request, 'ingreso.html', {'categories': categories,
                                                'subcategories': subcategories,
                                                })

def registro(request):

    registered = False

    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        userprofile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            print "user: ",user

            userprofile = userprofile_form.save(commit=False)
            userprofile.user = user
            userprofile.phone = userprofile_form.cleaned_data['phone']
            userprofile.register_date = datetime.now().date()
            userprofile.avg_reputation = 0
            userprofile.type_user = UserType.objects.get(id=1)
            userprofile.save()

            registered=True
        else:
            print user_form.errors,userprofile_form.errors


    else:
        user_form = UserForm()
        userprofile_form = UserProfileForm()

    return render(request, 'registro.html',
                  {'user_form': user_form,
                   'userprofile_form': userprofile_form,
                   'registered': registered,
                   'categories': categories,
                   'subcategories': subcategories,
                   }
                  )


def registra_social(request):
    registered = False

    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    if request.method == 'POST':
        userprofile_form = UserProfileForm(data=request.POST)

        if userprofile_form.is_valid():

            user = request.user

            userprofile = userprofile_form.save(commit=False)
            userprofile.user = user
            userprofile.phone = userprofile_form.cleaned_data['phone']
            userprofile.address = userprofile_form.cleaned_data['address']
            userprofile.register_date = datetime.now().date()
            userprofile.save()

            registered = True

            return render(request, 'registra_social.html', {'registered': registered,
                                                            })
        else:
            user = request.user
            real_user = User.objects.get(username=user)
            real_user.delete()

            registered = False
            print userprofile_form.errors

            return render(request, 'registra_social.html', {'registered': registered,
                                                            })


    else:
        userprofile_form = UserProfileForm()

    return render(request, 'registra_social.html',
                  {'userprofile_form': userprofile_form,
                   'registered': registered,
                   'categories': categories,
                   'subcategories': subcategories,
                   }
                  )

@login_required
def obsequiar(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    start_date = profile.register_date  # we obtain the register date of request user's
    enddate = date.today()  # date of today
    finish_date = enddate - start_date  # calculate the difference between enddate and startdate
    post_form = PostForm()
    picture_form = PictureForm()
    gift_form = GiftForm()
    can_posts = False

    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    if finish_date.days > 3:
        can_posts = True
        print "request method: ", request.method
        if request.method == 'POST':
            post_form = PostForm(data=request.POST)
            gift_form = GiftForm(data=request.POST)
            picture_form = PictureForm(data=request.POST)

            if picture_form.is_valid() and gift_form.is_valid() and post_form.is_valid():

                gift = gift_form.save(commit=False)
                gift.category = gift_form.cleaned_data['category']
                gift.subcategory = gift_form.cleaned_data['subcategory']
                gift.used_time_type = gift_form.cleaned_data['used_time_type']
                gift.dimension_type = gift_form.cleaned_data['dimension_type']
                gift.state_type = gift_form.cleaned_data['state_type']
                gift.weight_type = gift_form.cleaned_data['type_weight']
                gift.weight = gift_form.cleaned_data['weight']
                gift.save()

                picture = picture_form.save(commit=False)

                if 'picture' in request.FILES:
                    picture.picture = request.FILES['picture']

                picture.save()

                post = post_form.save(commit=False)
                post.user_post = request.user
                post.state_post = PostStateType.objects.get(id=1)  # recibiendo postulaciones
                post.title = post_form.cleaned_data['title']
                post.detail = post_form.cleaned_data['detail']
                post.finish_date = post_form.cleaned_data['finish_date']
                post.person2person_dispatch = post_form.cleaned_data['person2person_dispatch']
                post.pay_winner_dispatch = post_form.cleaned_data['pay_winner_dispatch']
                post.giver_pay_dispatch = post_form.cleaned_data['giver_pay_dispatch']
                post.according_to_winner_dispatch = post_form.cleaned_data['according_to_winner_dispatch']
                post.region = post_form.cleaned_data['region']
                post.provincia = post_form.cleaned_data['provincia']
                post.comuna = post_form.cleaned_data['comuna']
                post.gift = gift
                post.picture = picture
                post.save()

                return HttpResponseRedirect('/')

            else:
                print picture_form.errors, gift_form.errors, post_form.errors

        else:
            post_form = PostForm()
            picture_form = PictureForm()
            gift_form = GiftForm()

    else:
        return render(request, 'obsequiar.html',
                  {'picture_form':picture_form,
                   'gift_form':gift_form,
                   'post_form': post_form,
                   'can_posts': can_posts,
                   'categories': categories,
                   'subcategories': subcategories,
                   })

    return render(request, 'obsequiar.html',
                  {'picture_form': picture_form,
                   'gift_form': gift_form,
                   'post_form': post_form,
                   'can_posts': can_posts,
                   'categories': categories,
                   'subcategories': subcategories,
                   })

@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')


def faq(request):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    return render(request, 'faq.html', {'categories': categories,
                                        'subcategories': subcategories,
                                        })

def contacto(request):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    return render(request, 'contacto.html', {'categories': categories,
                                             'subcategories': subcategories,
                                             })

def quienes_somos(request):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    return render(request, 'quienes_somos.html', {'categories': categories,
                                                  'subcategories': subcategories,
                                                  })


@login_required
def checkout1(request, post_id):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    data = Post.objects.select_related('user_post').filter(id=post_id)
    user_visit = request.user

    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    if data.exists():
        post = Post.objects.get(id=post_id)
        gift = Gift.objects.get(post_gift=post)
        picture = Picture.objects.get(post_picture=post)
        user_post_id = post.user_post.id
        user_post = User.objects.get(id=user_post_id)
        profile = UserProfile.objects.get(user=user_post)
        postulation = Postulations.objects.get(post_postulation=post,
                                               winner=True,
                                               )
        user_postulation = postulation.user_postulation
        if request.method == 'POST':
            url = request.path
            url = url[:-2]
            url = url + '2'
            return HttpResponseRedirect(url)

    else:
        return index(request)

    return render(request, 'checkout1.html', {'post': post,
                                              'gift': gift,
                                              'picture': picture,
                                              'user_post_id': user_post_id,
                                              'user_post': user_post,
                                              'profile': profile,
                                              'postulation': postulation,
                                              'categories': categories,
                                              'subcategories': subcategories,
                                              'user_postulation': user_postulation,
                                              })


@login_required
def checkout2(request, post_id):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    data = Post.objects.select_related('user_post').filter(id=post_id)
    user_visit = request.user

    if data.exists():
        post = Post.objects.get(id=post_id)
        gift = Gift.objects.get(post_gift=post)
        picture = Picture.objects.get(post_picture=post)
        user_post_id = post.user_post.id
        user_post = User.objects.get(id=user_post_id)
        profile = UserProfile.objects.get(user=user_post)
        postulation = Postulations.objects.get(post_postulation=post,
                                               winner=True,
                                               )
        user_postulation = postulation.user_postulation

        if request.method == 'POST':
            url = request.path
            url = url[:-2]
            url = url + '3'
            return HttpResponseRedirect(url)
    else:
        return index(request)

    return render(request, 'checkout2.html', {'post': post,
                                              'gift': gift,
                                              'picture': picture,
                                              'user_post_id': user_post_id,
                                              'user_post': user_post,
                                              'profile': profile,
                                              'postulation': postulation,
                                              'user_postulation': user_postulation,
                                              # 'win_postulation':win_postulation,
                                              })


@login_required
def checkout3(request, post_id):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    data = Post.objects.select_related('user_post').filter(id=post_id)
    user_visit = request.user

    if data.exists():
        post = Post.objects.get(id=post_id)
        gift = Gift.objects.get(post_gift=post)
        picture = Picture.objects.get(post_picture=post)
        user_post_id = post.user_post.id
        user_post = User.objects.get(id=user_post_id)
        profile = UserProfile.objects.get(user=user_post)
        postulation = Postulations.objects.get(post_postulation=post,
                                               winner=True,
                                               )
        user_postulation = postulation.user_postulation
        if request.method == 'POST':
            url = request.path
            url = url[:-2]
            url = url + '4'
            return HttpResponseRedirect(url)
    else:
        return index(request)

    return render(request, 'checkout3.html', {'post':post,
                                              'gift':gift,
                                              'picture': picture,
                                              'user_post_id': user_post_id,
                                              'user_post':user_post,
                                              'profile': profile,
                                              'postulation': postulation,
                                              'user_postulation': user_postulation,
                                              # 'win_postulation':win_postulation,
                                              })


@login_required
def checkout4(request, post_id):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    data = Post.objects.select_related('user_post').filter(id=post_id)
    user_visit = request.user

    if data.exists():
        post = Post.objects.get(id=post_id)
        gift = Gift.objects.get(post_gift=post)
        picture = Picture.objects.get(post_picture=post)
        user_post_id = post.user_post.id
        user_post = User.objects.get(id=user_post_id)
        profile = UserProfile.objects.get(user=user_post)
        postulation = Postulations.objects.get(post_postulation=post,
                                               winner=True,
                                               )
        user_postulation = postulation.user_postulation

        if request.method == 'POST':
            post.state = False
            post.save()
            url = request.path
            url = url[:-10]
            url = url + 'evaluacion/'
            print url
            return HttpResponseRedirect(url)
    else:
        return index(request)

    return render(request, 'checkout4.html', {'post': post,
                                              'gift': gift,
                                              'picture': picture,
                                              'user_post_id': user_post_id,
                                              'user_post': user_post,
                                              'profile': profile,
                                              'postulation': postulation,
                                              'user_postulation': user_postulation,
                                              # 'win_postulation':win_postulation,
                                              })


@login_required
def ganador(request):
    if request.method == 'GET':
        id_postulation = request.GET['id_postulation']
        postulation = Postulations.objects.prefetch_related('post_postulation').get(id=id_postulation)
        id_post = postulation.post_postulation.id
        print id_post
        post = postulation.post_postulation
        url = '/post/' + str(id_post) + '/'
        url = url + 'checkout1/'

        notification = Notifications()
        notification.notified_user = postulation.user_postulation
        notification.title = 'Ganador de un obsequio!'
        notification.open = False
        notification.url = url

        postulation.winner = True
        postulation.post_postulation.state = False
        postulation.save()

        postulation.post_postulation.save()

        notification.save()
        # return render(request, 'post.html', {'post':post,
        #                                     })

        return HttpResponse(
            json.dumps(postulation),
            content_type="application/json",
        )

    else:
        return HttpResponse(
            json.dumps({"Nada para ver": "Esto no puede suceder!"}),
            content_type="application/json",
        )


@login_required
def seleccionado(request):
    if request.method == 'GET':
        id_postulation = request.GET['id_postulation']
        print id_postulation
        postulation = Postulations.objects.get(id=id_postulation)
        postulation.selected = True
        postulation.save()

        return HttpResponse(
            json.dumps(postulation),
            content_type="application/json",
        )

    else:
        return HttpResponse(
            json.dumps({"Nada para ver": "Esto no puede suceder!"}),
            content_type="application/json",
        )


@login_required
def evaluacion(request, post_id):
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    data = Post.objects.select_related('user_post').filter(id=post_id)
    user_visit = request.user

    if data.exists():
        post = Post.objects.get(id=post_id)
        gift = Gift.objects.get(post_gift=post)
        picture = Picture.objects.get(post_picture=post)
        user_post_id = post.user_post.id
        user_post = User.objects.get(id=user_post_id)
        profile = UserProfile.objects.get(user=user_post)
        postulation = Postulations.objects.filter(post_postulation=post)
        postulation = postulation.filter(winner=True)
        evaluation_form = EvaluationForm()

        if request.method == 'POST':

            evaluation_form = EvaluationForm(data=request.POST)

            if evaluation_form.is_valid():
                evaluation = evaluation_form.save(commit=False)
                profile.cant_evaluaciones = profile.cant_evaluaciones + 1
                profile.save()
                cant_evals = profile.cant_evaluaciones
                eval = evaluation.avg_reputation
                avg = profile.avg_reputation
                new_avg = (int(eval) + int(avg)) / int(cant_evals)
                print new_avg
                # tipo usuario no confiable
                if new_avg < 2:
                    user_type = UserType.objects.get(id=8)
                    profile.type_user = user_type
                # tipo usuario confiable
                if new_avg >= 2 and new_avg < 5:
                    user_type = UserType.objects.get(id=6)
                    profile.type_user = user_type
                # tipo usuario recomendado
                if new_avg >= 5:
                    user_type = UserType.objects.get(id=7)
                    profile.type_user = user_type
                profile.avg_reputation = int(new_avg)
                profile.save()
                post.state = False
                post.save()
                return HttpResponseRedirect('/')
            else:
                print evaluation_form.errors


    else:
        return index(request)

    return render(request, 'evaluacion.html', {'post': post,
                                               'gift': gift,
                                               'picture': picture,
                                               'user_post_id': user_post_id,
                                               'user_post': user_post,
                                               'profile': profile,
                                               'postulation': postulation,
                                               'evaluation_form': evaluation_form,
                                               # 'win_postulation':win_postulation,
                                               'categories': categories,
                                               'subcategories': subcategories,
                                               })


@login_required
def like_post(request, post_id):
    id_post = None
    if request.method == 'GET':
        id_post = request.GET['post_id']

    likes = 0
    if id_post:
        post = Post.objects.get(id=int(id_post))
        if post:
            likes = post.num_likes + 1
            post.num_likes = likes
            post.save()

    return HttpResponse(likes)


@login_required
def read_notificacion(request):
    if request.method == 'GET':
        id_notificacion = request.GET['notificationid']
        print id_notificacion
        notification = Notifications.objects.get(id=id_notificacion)
        notification.open = True
        notification.save()

        return HttpResponse(
            json.dumps(notification),
            content_type="application/json",
        )

    else:
        return HttpResponse(
            json.dumps({"Nada para ver": "Esto no puede suceder!"}),
            content_type="application/json",
        )


def get_provincias(request):
    if request.method == 'GET' and request.is_ajax():
        region_name = request.GET['name_region']
        region = RegionPost.objects.get(region_name=region_name)
        provincias = ProvinciaPost.objects.filter(region=region.id).values()
        list_provincias = list(provincias)
        json_data = json.dumps(list_provincias)

    return HttpResponse(json_data, content_type='application/json')


def get_comunas(request):
    if request.method == 'GET' and request.is_ajax():
        name_provincia = request.GET['name_provincia']
        provincia = ProvinciaPost.objects.get(provincia_name=name_provincia)
        comunas = ComunaPost.objects.filter(provincia=provincia.id).values()
        list_comunas = list(comunas)
        json_data = json.dumps(list_comunas)

    return HttpResponse(json_data, content_type='application/json')


def get_subcategories(request):
    if request.method == 'GET' and request.is_ajax():
        name_category = request.GET['name_category']
        category = CategoryGift.objects.get(name_category=name_category)
        subcategories = SubcategoryGift.objects.filter(category=category.id).values()
        list_subcategories = list(subcategories)
        json_data = json.dumps(list_subcategories)

    return HttpResponse(json_data, content_type='application/json')

@login_required
def profile(request):
    request_user = request.user
    user = User.objects.get(id=request_user.id)
    user_profile = UserProfile.objects.get(user=user)
    print "user_profile picture", user_profile.picture
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get("firstname", "")
        last_name = request.POST.get("lastname", "")
        phone = request.POST.get("phone", "")
        mail = request.POST.get("email", "")
        user.first_name = first_name
        user.last_name = last_name
        user.email = mail
        user_profile.phone = phone
        user.save()
        user_profile.save()

        return render(request, 'profile.html', {'user': user,
                                                'user_profile': user_profile,
                                                'categories': categories,
                                                'subcategories': subcategories,
                                                })

    return render(request, 'profile.html', {'user': user,
                                            'user_profile': user_profile,
                                            'categories': categories,
                                            'subcategories': subcategories,
                                            })


@login_required
def my_gifts(request):
    request_user = request.user
    user = User.objects.get(id=request_user.id)
    user_profile = UserProfile.objects.get(user=user)
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    return render(request, 'my_gifts.html', {'user': user,
                                             'user_profile': user_profile,
                                             'categories': categories,
                                             'subcategories': subcategories,
                                             })


@login_required
def my_postulations(request):
    request_user = request.user
    user = User.objects.get(id=request_user.id)
    user_profile = UserProfile.objects.get(user=user)
    notifications = Notifications.objects.filter(notified_user=user.id)
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    return render(request, 'my_postulations.html', {'user': user,
                                                    'user_profile': user_profile,
                                                    'categories': categories,
                                                    'subcategories': subcategories,
                                                    'notifications': notifications,
                                                    })


@login_required
def my_notifications(request):
    request_user = request.user
    print request_user
    user = User.objects.get(id=request_user.id)
    print user
    user_profile = UserProfile.objects.get(user=user)
    notifications = Notifications.objects.filter(notified_user=user, open=False).values()  # open=False
    print notifications
    categories = CategoryGift.objects.all()
    subcategories = SubcategoryGift.objects.all()

    return render(request, 'my_notifications.html', {'user': user,
                                                     'user_profile': user_profile,
                                                     'categories': categories,
                                                     'subcategories': subcategories,
                                                     'notifications': notifications,
                                                     })
